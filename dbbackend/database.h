#include <sstream>
#include <map>
#include <unordered_map>
#include "user.h"

class Database
{
public:
  Database(std::string);

  Database(std::string, std::string);

  void reload(std::string);

  int size() const { return db_users.size(); }

  User findById(int);

  std::vector<User> findByName(std::string);

  std::vector<User*> query(std::string);

  std::string text()
  {
    std::stringstream ss;
    for (auto u : db_users)
    {
      ss << u.second.text() << std::endl;
    }
    return ss.str();
  };

  std::unordered_map<int, std::string> *getZipCodes() { return &zip_codes; };

  int loadAvatars(std::string);

private:
  std::unordered_map<int, User> db_users;
  std::multimap<std::string, int> inverse_db_users;
  std::unordered_map<int, std::string> zip_codes;
};
