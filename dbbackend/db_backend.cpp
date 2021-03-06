#include "SHTTP/server_http.hpp"
#include "database.h"

#define BOOST_SPIRIT_THREADSAFE
#include <boost/property_tree/json_parser.hpp>
#include <boost/property_tree/ptree.hpp>

#include <algorithm>
#include <boost/filesystem.hpp>
#include <fstream>
#include <vector>

using namespace std;
using namespace boost::property_tree;

using HttpServer = SimpleWeb::Server<SimpleWeb::HTTP>;

int main()
{
  cout << "Reading db file ..." << std::endl;
  string db_file = "/home/cwc-work/bot/botcoco/dbbackend/users_dev";
  string zip_codes = "/home/cwc-work/bot/botcoco/cocoweb/conf/zip-codes.txt";
  string avatar_folder = "/home/cwc-work/bot/botcoco/crawler/avatars/";
  Database db(db_file, zip_codes);
  cout << "Finished reading db" << std::endl;
  // std::cout << db.text() << std::endl;
  cout << "Contains: " << db.size() << std::endl;
  int avs = db.loadAvatars(avatar_folder);
  cout << "Loaded " << avs << " avatars" << std::endl;

  HttpServer server;
  server.config.port = 8080;

  server.resource["^/info$"]["GET"] = [](shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request) {
    stringstream stream;
    stream << "<h1>Request from " << request->remote_endpoint_address() << ":" << request->remote_endpoint_port() << "</h1>";

    stream << request->method << " " << request->path << " HTTP/" << request->http_version;

    stream << "<h2>Query Fields</h2>";
    auto query_fields = request->parse_query_string();
    for (auto &field : query_fields)
      stream << field.first << ": " << field.second << "<br>";

    stream << "<h2>Header Fields</h2>";
    for (auto &field : request->header)
      stream << field.first << ": " << field.second << "<br>";

    response->write(stream);
  };

  server.resource["^/update$"]["GET"] = [&db, &db_file, &avatar_folder](shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> /* request */) {
    thread work_thread([response, &db, db_file, avatar_folder] {
      cout << "reloading database ..." << endl;
      db.reload(db_file);
      cout << "Contains: " << db.size() << std::endl;
      int avs = db.loadAvatars(avatar_folder);
      cout << "Loaded " << avs << " avatars" << std::endl;

      *response << "HTTP/1.1 200 OK\r\n"
                << "Content-Length: " << 0 << "\r\n"
                << "Access-Control-Allow-Origin: *"
                << "\r\n"
                << "\r\n";
    });
    work_thread.detach();
  };

  // ^\/find\/\?(((uid)|(city))=([0-9])+)(&(((uid)|(city))=([0-9])+))+ for /find/?uid=342&city=342
  server.resource["^/uid/([0-9]{6})"]["GET"] = [&db](shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request) {
    // std::string req = request->content.string(); // can be used with -d option in curl (curl -X GET -d 'something' link:port)
    std::string uid_string = request->path_match[1];
    int uid = stoi(uid_string);
    User x = db.findById(uid);
    string resp_text;

    resp_text = x.json(db.getZipCodes());

    *response << "HTTP/1.1 200 OK\r\n"
              << "Content-Length: " << resp_text.length() << "\r\n"
              << "Access-Control-Allow-Origin: *"
              << "\r\n"
              << "\r\n"
              << resp_text;
  };

  server.resource["^/pseudo/([a-zA-Z0-9]+)"]["GET"] = [&db](shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request) {
    std::string name = request->path_match[1];
    std::vector<User> x = db.findByName(name);
    string resp_text;

    std::stringstream ss;
    ss << "{\"total\":" << x.size() << ",\"users\":[";
    for (User u : x)
    {
      ss << u.json(db.getZipCodes()) << ",";
    }
    if (!x.empty())
      ss.seekp(-1, ss.cur); // to remove the last ','
    ss << "]}";
    resp_text = ss.str();

    *response << "HTTP/1.1 200 OK\r\n"
              << "Content-Length: " << resp_text.length() << "\r\n"
              << "Access-Control-Allow-Origin: *"
              << "\r\n"
              << "\r\n"
              << resp_text;
  };

  server.resource["^/query/([a-zA-Z0-9]+)"]["GET"] = [&db](shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request) {
    std::string name = request->path_match[1];
    std::vector<User *> x = db.query(name);
    string resp_text;

    std::stringstream ss;
    ss << "{\"total\":" << x.size() << ",\"users\":[";
    for (User *u : x)
    {
      ss << u->json(db.getZipCodes()) << ",";
    }
    if (!x.empty())
      ss.seekp(-1, ss.cur); // to remove the last ','
    ss << "]}";
    resp_text = ss.str();

    *response << "HTTP/1.1 200 OK\r\n"
              << "Content-Length: " << resp_text.length() << "\r\n"
              << "Access-Control-Allow-Origin: *"
              << "\r\n"
              << "\r\n"
              << resp_text;
  };

  server.resource["^/([0-9]{6}-[0-9]{3}\\.jpg)"]["GET"] = [&avatar_folder](shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request) {
    std::string avatar_name = request->path_match[1];
    try
    {
      auto avatars_root_path = boost::filesystem::canonical(avatar_folder);
      auto path = boost::filesystem::canonical(avatars_root_path / avatar_name);

      SimpleWeb::CaseInsensitiveMultimap header;

      auto ifs = make_shared<ifstream>();
      ifs->open(path.string(), ifstream::in | ios::binary | ios::ate);

      if (*ifs)
      {
        auto length = ifs->tellg();
        ifs->seekg(0, ios::beg);

        header.emplace("Content-Length", to_string(length));
        header.emplace("Access-Control-Allow-Origin", "*");
        response->write(header);

        class FileServer
        {
        public:
          static void read_and_send(const shared_ptr<HttpServer::Response> &response, const shared_ptr<ifstream> &ifs)
          {
            static vector<char> buffer(131072);
            streamsize read_length;
            if ((read_length = ifs->read(&buffer[0], static_cast<streamsize>(buffer.size())).gcount()) > 0)
            {
              response->write(&buffer[0], read_length);
              if (read_length == static_cast<streamsize>(buffer.size()))
              {
                response->send([response, ifs](const SimpleWeb::error_code &ec) {
                  if (!ec)
                    read_and_send(response, ifs);
                  else
                    cerr << "Connection interrupted" << endl;
                });
              }
            }
          }
        };
        FileServer::read_and_send(response, ifs);
      }
      else
        throw invalid_argument("could not read file");
    }
    catch (const exception &e)
    {
      response->write(SimpleWeb::StatusCode::client_error_bad_request, "Could not open path " + avatar_name);
    }
  };

  /*
  server.resource["^/query"]["GET"] = [](shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request) {
    thread work_thread([response] {
      this_thread::sleep_for(chrono::seconds(5));
      response->write("Work done");
    });
    work_thread.detach();
  };
  */

  server.default_resource["GET"] = [](shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request) {
    try
    {
      auto web_root_path = boost::filesystem::canonical("web");
      auto path = boost::filesystem::canonical(web_root_path / request->path);
      // Check if path is within web_root_path
      if (distance(web_root_path.begin(), web_root_path.end()) > distance(path.begin(), path.end()) ||
          !equal(web_root_path.begin(), web_root_path.end(), path.begin()))
        throw invalid_argument("path must be within root path");
      if (boost::filesystem::is_directory(path))
        path /= "index.html";

      SimpleWeb::CaseInsensitiveMultimap header;

      // Uncomment the following line to enable Cache-Control
      // header.emplace("Cache-Control", "max-age=86400");

      auto ifs = make_shared<ifstream>();
      ifs->open(path.string(), ifstream::in | ios::binary | ios::ate);

      if (*ifs)
      {
        auto length = ifs->tellg();
        ifs->seekg(0, ios::beg);

        header.emplace("Content-Length", to_string(length));
        response->write(header);

        // Trick to define a recursive function within this scope (for example purposes)
        class FileServer
        {
        public:
          static void read_and_send(const shared_ptr<HttpServer::Response> &response, const shared_ptr<ifstream> &ifs)
          {
            // Read and send 128 KB at a time
            static vector<char> buffer(131072); // Safe when server is running on one thread
            streamsize read_length;
            if ((read_length = ifs->read(&buffer[0], static_cast<streamsize>(buffer.size())).gcount()) > 0)
            {
              response->write(&buffer[0], read_length);
              if (read_length == static_cast<streamsize>(buffer.size()))
              {
                response->send([response, ifs](const SimpleWeb::error_code &ec) {
                  if (!ec)
                    read_and_send(response, ifs);
                  else
                    cerr << "Connection interrupted" << endl;
                });
              }
            }
          }
        };
        FileServer::read_and_send(response, ifs);
      }
      else
        throw invalid_argument("could not read file");
    }
    catch (const exception &e)
    {
      response->write(SimpleWeb::StatusCode::client_error_bad_request, "Could not open path " + request->path + ": " + e.what());
    }
  };

  server.on_error = [](shared_ptr<HttpServer::Request> /*request*/, const SimpleWeb::error_code & /*ec*/) {
    // Handle errors here
    // Note that connection timeouts will also call this handle with ec set to SimpleWeb::errc::operation_canceled
  };

  thread server_thread([&server]() {
    // Start server
    server.start();
  });

  // Wait for server to start so that the client can connect
  this_thread::sleep_for(chrono::seconds(1));

  server_thread.join();
}
