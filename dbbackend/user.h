#include <sstream>
#include <vector>
#include <set>
#include <time.h>

class Pseudo
{
public:
  Pseudo(std::string pseudo_line)
  {
    std::istringstream f(pseudo_line);
    std::string s;
    std::getline(f, s, '|');
    name = s;
    std::getline(f, s, '|');
    struct tm tm;
    strptime(s.c_str(), "%d/%m/%Y-%H:%M", &tm);
    timestamp = mktime(&tm);
  };

  std::string text()
  {
    std::stringstream ss;
    ss << name;
    return ss.str();
  }

  std::string getName()
  {
    return name;
  }

  std::string json()
  {
    std::stringstream ss;
    ss << "{\"name\":\"" << name << "\"}";
    return ss.str();
  }

private:
  std::string name;
  std::time_t timestamp;
};

class User
{
public:
  User()
  {
    uid = -1;
    city = 0;
    age = 0;
  }

  User(std::string dbline)
  {
    std::istringstream f(dbline);
    std::string s;
    std::getline(f, s, ';');
    uid = std::stoi(s);
    std::getline(f, s, ';');
    std::istringstream p(s);
    std::string ps;
    while (std::getline(p, ps, ','))
    {
      pseudos.emplace_back(ps);
    }
    std::getline(f, s, ';');
    age = std::stoi(s);
    std::getline(f, s, ';');
    city = std::stoi(s);
  };

  std::string text()
  {
    std::stringstream ss;
    ss << pseudos[0].text() << " " << uid << " " << city;
    return ss.str();
  };

  std::string json(std::unordered_map<int, std::string>* zip_codes)
  {
    std::stringstream ss;
    ss << "{\"id\":"<<uid<<",\"city\":\""<<(*zip_codes)[city]<<"\",\"age\":"<<age;
    // adding pseudos' list
    ss << ",\"pseudos\":[";
    for (Pseudo p : pseudos)
    {
      ss << p.json() << ",";
    }
    ss.seekp(-1, ss.cur);// to remove the last ','
    ss << "]";
    // adding avatars' list
    ss << ",\"avatars\":[";
    for (std::string p : avatars)
    {
      ss << "\"" << p << "\",";
    }
    if (!avatars.empty())
      ss.seekp(-1, ss.cur);// to remove the last ','
    ss << "]";
    // closing
    ss << "}";
    return ss.str();
  }

  inline int getUid() const { return uid; };

  inline std::string getName() {return pseudos[0].text();};

  void addAvatar(std::string link) { avatars.push_back(link); }

  inline std::set<std::string> getNames() {
    std::set<std::string> names;
    for (auto p : pseudos)
      names.insert(p.getName());
    return names;
  };

private:
  int uid;
  int city;
  int age;
  std::vector<Pseudo> pseudos;
  std::vector<std::string> avatars;
};
