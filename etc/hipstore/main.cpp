#include <fstream>
#include <iostream>
#include <filesystem>
#include <algorithm>
#include <cstring>
#include <iterator>
//#include <signal.h>
#include <unistd.h>
//#include "libgen.h"

namespace fs = std::filesystem;


struct User {
    char password[128];
    bool VIP = false;
    char name[128];
    //size_t money = 1000;
    int money = 1000;
    size_t spinners;
    size_t vapes;
    double discount = 0.05;
    unsigned int token;
    //char review[256];
    std::string review;
};

unsigned int CRC32_function(unsigned char *buf, unsigned long len);
void printListUsers();
User *checkToken(uint64_t token);
void saveToDb(User *user);
void getReviewUserSpinners();
void getReviewByName(std::string name);
bool getUserList(const char * name);
void getUserList();

unsigned int genToken(char * name) {

    return CRC32_function((unsigned char *)name, strlen(name));
}

unsigned int genToken(std::string &name) {

    return CRC32_function((unsigned char *)name.c_str(), 255);
}




void saveUser(char * name) {
    std::ofstream out("users/list_users.txt", std::ios::app);
    out << name << "_";
}

User *registerUser() {
    User *ret = new User;
//    std::cout << "Enter len: ";
//    unsigned short lenUsername = 256;
//    std::cin >> lenUsername;
//    std::cout << std::endl;
//    std::cout << "Enter len pass: ";
    unsigned short lenPassword = 256;
//    std::cin >> lenPassword;
//    std::cout << std::endl;

    std::cout << "Your username?" << std::endl;
    std::cin.getline(ret->name, 256);
    if (getUserList(ret->name)) {
        std::cout << "Username alread exist!" << std::endl;
        exit(0);
    };
    std::cout << "Your password?" << std::endl;
    std::cin.getline(ret->password, 256);
    ret->token = genToken(ret->name);
    std::cout << "Your money: " << ret->money << std::endl;
    std::cout << "Your token is: " << std::hex << ret->token << std::endl;
    std::cout << std::dec << std::endl;

    saveUser(ret->name);
    //saveToDb(ret);
    return ret;
}

struct AtheaModsGimmick {
    size_t salary = 1000;
} amg;

struct PredatorCapS
{
    size_t salary = 500;
} pcs;


struct MonsterVaporVapex
{
    size_t salary = 100;
} mvv;



struct CaviarSpinnerTricolor
{
    size_t salary = 1000;
} cst;

struct iPhoneFidgetSpinner
{
    size_t salary = 500;
} ipfs;

struct AtessonFidgetSpinner
{
    size_t salary = 20;
} afs;


void saveToDb(User *user) {
    //ToDo: check existing directory users
    //fs::create_directory("users");
    std::ofstream myfile;
    //cast int to hex string
    std::stringstream stream;
    stream << std::hex << user->token;
    std::string result( stream.str() );

    std::replace(user->review.begin(), user->review.end(), ' ', '_');

    myfile.open ("users/" + result);
    myfile << user->name            << "\n";
//    myfile << user->VIP             << "\n";
    myfile << user->password        << "\n";
    myfile << user->money           << "\n";
    myfile << user->spinners        << "\n";
    myfile << user->vapes           << "\n";
    myfile << user->discount * 100  << "\n";
    myfile << user->token           << "\n";
    myfile << user->review          << "\n";
    myfile << user->VIP             << "\n";
    myfile.close();
}

void viewShop(User *user) {


    bool isEnd = false;
    while(!isEnd) {

        std::cout << "\nSpinners: \n"
                     "1.Caviar Spinner Tricolor: 1000$\n"
                     "2.iPhone Fidget Spinner: 500$\n"
                     "3.Atesson Fidget Spinner: 20$\n\n"
                     "Vapes: \n"
                     "4.Athea Mods Gimmick: 1000$\n"
                     "5.Predator Cap S: 500$\n"
                     "6.Monster Vapor Vapex: 100$\n"
                     "7.Buy buy user feedback (not legal): 1337$\n"
                     "8.Quit\n\n"
                  << std::endl;

        std::cout << "Your discount: " << user->discount << std::endl;
        std::cout << "Enter number: " << std::endl;


        size_t cmd;
        std::string s_cmd;
        std::getline(std::cin, s_cmd);
        try {
            cmd = std::stoi(s_cmd);
        } catch(...) {
            cmd = 0;
        }

        switch (cmd) {
            case 1: {
                std::cout << "You choosed Caviar Spinner Tricolor" << std::endl;
                if (user->money - static_cast<int>(static_cast<double>(cst.salary) - static_cast<double>(cst.salary) * user->discount) >= 0) {
                    user->money -= static_cast<int>(static_cast<double>(cst.salary) - static_cast<double>(cst.salary) * user->discount);
                    user->discount += 0.1;
                    std::cout << "Success!\n"
                                 "Your money: \n" << user->money
                              << "\nYour discount: \n" << static_cast<size_t >(user->discount * 100) << "%"
                              << std::endl;

                    user->spinners += 1;
                    std::cout << "Write your review please: " << std::endl;
                    std::getline(std::cin, user->review);
                }
                break;
            }
            case 2: {
                std::cout << "You choosed iPhone Fidget Spinner" << std::endl;
                if (user->money - static_cast<int>(static_cast<double>(ipfs.salary) - static_cast<double>(ipfs.salary) * user->discount) >= 0) {
                    user->money -= static_cast<int>(static_cast<double>(ipfs.salary) - static_cast<double>(ipfs.salary) * user->discount);
                    user->discount += 0.1;
                    std::cout << "Success!\n"
                                 "Your money: \n" << user->money
                              << "\nYour discount: \n" << static_cast<size_t >(user->discount * 100) << "%"
                              << std::endl;

                    user->spinners += 1;
                    std::cout << "Write your review please: " << std::endl;
                    std::getline(std::cin, user->review);
                }
                break;
            }
            case 3: {
                std::cout << "You choosed Atesson Fidget Spinner" << std::endl;
                if (user->money - static_cast<int>(static_cast<double>(afs.salary) - static_cast<double>(afs.salary) * user->discount) >= 0) {
                    user->money -= static_cast<int>(static_cast<double>(afs.salary) - static_cast<double>(afs.salary) * user->discount);
                    user->discount += 0.1;
                    std::cout << "Success!\n"
                                 "Your money: \n" << user->money
                              << "\nYour discount: \n" << static_cast<size_t >(user->discount * 100) << "%"
                              << std::endl;

                    user->spinners += 1;
                    std::cout << "Write your review please: " << std::endl;
                    std::getline(std::cin, user->review);
                }
                break;
            }
            case 4: {
                std::cout << "You choosed Athea Mods Gimmick" << std::endl;
                if (user->money - static_cast<int>(static_cast<double>(amg.salary) - static_cast<double>(amg.salary) * user->discount) >= 0) {
                    user->money -= static_cast<int>(static_cast<double>(amg.salary) - static_cast<double>(amg.salary) * user->discount);
                    user->discount += 0.1;
                    std::cout << "Success!\n"
                                 "Your money: \n" << user->money
                              << "\nYour discount: \n" << static_cast<size_t >(user->discount * 100) << "%"
                              << std::endl;

                    user->vapes += 1;
                    std::cout << "Write your review please: " << std::endl;
                    std::getline(std::cin, user->review);
                }
                break;
            }
            case 5: {
                std::cout << "You choosed Predator Cap S" << std::endl;
                if (user->money - static_cast<int>(static_cast<double>(pcs.salary) - static_cast<double>(pcs.salary) * user->discount) >= 0) {
                    user->money -= static_cast<int>(static_cast<double>(pcs.salary) - static_cast<double>(pcs.salary) * user->discount);
                    user->discount += 0.1;
                    std::cout << "Success!\n"
                                 "Your money: \n" << user->money
                              << "\nYour discount: \n" << static_cast<size_t >(user->discount * 100) << "%"
                              << std::endl;

                    user->vapes += 1;
                    std::cout << "Write your review please: " << std::endl;
                    std::getline(std::cin, user->review);
                }
                break;
            }

            case 6: {
                std::cout << "You choosed Monster Vapor Vapex" << std::endl;
                if (user->money - static_cast<int>(static_cast<double>(mvv.salary) - static_cast<double>(mvv.salary) * user->discount) >= 0) {
                    user->money -= static_cast<int>(static_cast<double>(mvv.salary) - static_cast<double>(mvv.salary) * user->discount);
                    user->discount += 0.05;
                    //user->discount += 0.5;
                    std::cout << "Success!\n"
                                 "Your money: \n" << user->money
                              << "\nYour discount: \n" << static_cast<size_t >(user->discount * 100) << "%"
                              << std::endl;

                    user->vapes += 1;
                    std::cout << "Write your review please: " << std::endl;
                    std::getline(std::cin, user->review);
                }
                break;
            }
            case 7: {
                // ToDo make a normal cast
                if (user->money >= 1337) {
                    getUserList();
                    std::cout << "Enter username: ";
                    std::string user;
                    std::getline(std::cin, user);
                    const char *tmp = user.c_str();
                    char name1[256] = {0};
                    strncpy(name1, tmp, 255);
                    uint64_t token = genToken(name1);
                    User *ret = new User;
                    ret = checkToken(token);
                    if (ret->token == 0)
                        std::cout << "User (token) not found" << std::endl;
                    else {
                        if (ret->vapes > 0)
                            std::cout << "review of " << name1 << "is " << ret->review << std::endl;
                    }
                }
                else
                    std::cout << "You have no enough money!" << std::endl;
                break;
            }
            case 8: {
                    isEnd = true;
                    break;
            }
            case 9: {
                if (user->VIP) {
                        getReviewUserSpinners();
                }
                break;
            }
            default: {
                break;
            }

        }
    }


    saveToDb(user);
}

bool demo_exists(const fs::path& p, fs::file_status s = fs::file_status{})
{
    if(fs::status_known(s) ? fs::exists(s) : fs::exists(p))
        return true;
    else
        return false;
}


User *checkToken(uint64_t token) {
    for(auto it = fs::directory_iterator("users"); it != fs::directory_iterator(); ++it)
        if (demo_exists(*it, it->status())) {// use cached status from directory entry
            User * user = new User;

            std::stringstream stream;
            stream << std::hex << token;
            std::string result( stream.str() );
            std::ifstream in("users/" + result);

            in >> user->name >> user->password >> user->money >> user->spinners
               >> user->vapes >> user->discount >> user->token >> user->review >> user->VIP;
            in.close();
            return user;
        }
    return (User *)0;
}
void printUser(User * user) {
    std::cout       << "Name: "  << user->name <<
    "\nVIP: "       <<  user->VIP <<
    "\npassword: "  << user->password <<
    "\nmoney: "     << user->money <<
    "\nspinners: "  << user->spinners <<
    "\nvapers: "    << user->vapes <<
    "\ndiscount: "  << user->discount <<
    "\ntoken: "     << std::hex << user->token <<
    "\nreview: "    << user->review << std::endl;

    std::cout << std::dec << std::endl;
}

void printListUsers() {
    std::string listUsers;
    std::fstream f("users/list_users.txt");
    f >> listUsers;
    std::replace(listUsers.begin(), listUsers.end(), '_', '\n');
    f.close();
    std::cout << listUsers << std::endl;
}



int main() {
    // ToDo may be save data of users rigth away after registration?

    alarm(10);


    fs::create_directory("users");
    std::cout << "Welcome to our hipstore service!\nHere you can purchase spinners and vapers!" << std::endl;
    bool isEnd = false;
    User *currentUser = nullptr;

    while (!isEnd) {
        std::cout << "Choose your action:\n"
                     "1.Register\n"
                     "2.Go to shop\n"
                     "3.List users\n"
                     "4.Authorization \n"
                     "5.My purchases \n"
                     "6.Quit\n" << std::endl;


        size_t cmd;
        std::string s_cmd;
        std::getline(std::cin, s_cmd);
        try {
            cmd = std::stoi(s_cmd);
        } catch (...) {
            cmd = 5;
        }

        switch (cmd) {
            case 1: {
                currentUser = registerUser();
                break;
            }
            case 2: {
                if (currentUser == nullptr) {
                    std::cout << "You should register first!" << std::endl;
                } else {
                    viewShop(currentUser);
                }
                break;
            }
            case 3: {
//                printListUsers();
                getUserList();
                break;
            }
            case 4: {
                std::cout << "Enter your token: " << std::endl;
                uint64_t token;
                std::cin >> std::hex >> token;
                currentUser = checkToken(token);
                if (currentUser->token == 0) {
                    std::cout << "token not found" << std::endl;
                    return 0;
                }
                break;
            }

            case 5: {
                if (currentUser == nullptr) {
                    std::cout << "You should register first!" << std::endl;
                } else {
                    printUser(currentUser);
                }
                break;
            }

            case 6: {
                isEnd = true;
                break;
            }
            default: {
                break;
            }
        }
    }
}

void getReviewUserSpinners() {
    std::string listUsers;
    std::fstream f("users/list_users.txt");
    f >> listUsers;
    f.close();
    std::replace(listUsers.begin(), listUsers.end(), '_', ' ');
    //std::cout << listUsers << std::endl;
    std::stringstream ss(listUsers);
    std::istream_iterator<std::string> begin(ss);
    std::istream_iterator<std::string> end;
    std::vector<std::string> vstrings(begin, end);
    //std::copy(vstrings.begin(), vstrings.end(), std::ostream_iterator<std::string>(std::cout, "\n"));

    std::cout << std::endl;

    for (const auto &val : vstrings) {
        getReviewByName(val);
    }
}

void getReviewByName(std::string name) {
    auto token = genToken((char *)name.c_str());
    std::cout << name << " " << std::hex << token << std::dec << " ";
    User *ret = new User;
    ret = checkToken(token);
    if (ret->token == 0)
        std::cout << "User (token) not found" << std::endl;
    else {
        if (ret->spinners > 0)
            std::cout << "review of " << name << "is " << ret->review << std::endl;
    }

}


unsigned int CRC32_function(unsigned char *buf, unsigned long len)
{
    unsigned long crc_table[256];
    unsigned long crc;
    for (int i = 0; i < 256; i++)
    {
        crc = i;
        for (int j = 0; j < 8; j++)
            crc = crc & 1 ? (crc >> 1) ^ 0xEDB88320UL : crc >> 1;
        crc_table[i] = crc;
    };
    crc = 0xFFFFFFFFUL;
    while (len--)
        crc = crc_table[(crc ^ *buf++) & 0xFF] ^ (crc >> 8);
    return crc ^ 0xFFFFFFFFUL;
}


bool getUserList(const char * name) {
    std::string listUsers;
    std::fstream f("users/list_users.txt");
    f >> listUsers;
    f.close();
    std::replace(listUsers.begin(), listUsers.end(), '_', ' ');
    std::stringstream ss(listUsers);
    std::istream_iterator<std::string> begin(ss);
    std::istream_iterator<std::string> end;
    std::vector<std::string> vstrings(begin, end);
//    std::copy(vstrings.begin(), vstrings.end(), std::ostream_iterator<std::string>(std::cout, "\n"));


    if (std::find(vstrings.begin(), vstrings.end(), name) != vstrings.end())
        return true;
        //std::cout << "User " << name << " is exist!!!";

//    for (const auto &val : vstrings) {
//        std::cout << val << " ";
//    }
    return false;

}

void getUserList() {
    std::string listUsers;
    std::fstream f("users/list_users.txt");
    f >> listUsers;
    f.close();
    std::replace(listUsers.begin(), listUsers.end(), '_', ' ');
    std::stringstream ss(listUsers);
    std::istream_iterator<std::string> begin(ss);
    std::istream_iterator<std::string> end;
    std::vector<std::string> vstrings(begin, end);
    std::vector<std::string> tenUsers(vstrings.end() - 10, vstrings.end());
//    std::copy(vstrings.begin(), vstrings.end(), std::ostream_iterator<std::string>(std::cout, "\n"));

    //std::cout << "User " << name << " is exist!!!";

    for (const auto &val : tenUsers) {
        std::cout << val << std::endl;
    }
}