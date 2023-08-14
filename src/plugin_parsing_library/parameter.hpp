#ifndef PARAMETER_H
#define PARAMETER_H
#include <string>
#include <string.h>
#include <yaml-cpp/yaml.h>

class parameter{

    public: //talvez mudar depois

    std::string name;
    std::string human_readable_name;
    std::string tag_name;
    std::string description;
    std::string type;
    bool required;

    parameter(  std::string _name,
            std::string _human_readable_name,
            std::string _tag_name,
            std::string _description,
            std::string _type,
            bool _required);

};

class string_parameter : public parameter{

    public: //same

    std::string value;
    std::string default_value;

    string_parameter( std::string _name,
                    std::string _human_readable_name,
                    std::string _tag_name,
                    std::string _description,
                    std::string _type,
                    bool _required,
                    std::string _default_value);

};

class topic_name : public string_parameter {

    public:

    topic_name( std::string _name,
            std::string _human_readable_name,
            std::string _tag_name,
            std::string _description,
            std::string _type,
            bool _required,
            std::string _default_value);

};

class link_reference : public string_parameter {

    public:

    link_reference( std::string _name,
            std::string _human_readable_name,
            std::string _tag_name,
            std::string _description,
            std::string _type,
            bool _required,
            std::string _default_value);

};

class joint_reference : public string_parameter {

    public:

    joint_reference( std::string _name,
            std::string _human_readable_name,
            std::string _tag_name,
            std::string _description,
            std::string _type,
            bool _required,
            std::string _default_value);

};

class model_reference : public string_parameter {

    public:

    model_reference( std::string _name,
            std::string _human_readable_name,
            std::string _tag_name,
            std::string _description,
            std::string _type,
            bool _required,
            std::string _default_value);

};

class double_parameter : public parameter{

    public:

    double value;
    double default_value;

    double_parameter(  std::string _name,
                    std::string _human_readable_name,
                    std::string _tag_name,
                    std::string _description,
                    std::string _type,
                    bool _required,
                    double _default_value);

};

class integer_parameter : public parameter{

    public:

    int value;
    int default_value;

    integer_parameter(  std::string _name,
                    std::string _human_readable_name,
                    std::string _tag_name,
                    std::string _description,
                    std::string _type,
                    bool _required,
                    int _default_value);

};

#endif