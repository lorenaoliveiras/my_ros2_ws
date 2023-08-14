#include "parameter.hpp"

// ------------------ constructors ------------------------

parameter::parameter(   std::string _name,
                        std::string _human_readable_name,
                        std::string _tag_name,
                        std::string _description,
                        std::string _type,
                        bool _required) {

    this->name                = _name;
    this->human_readable_name = _human_readable_name;
    this->tag_name            = _tag_name;
    this->description         = _description;
    this->type                = _type;
    this->required            = _required;

}

string_parameter::string_parameter( std::string _name,
                    std::string _human_readable_name,
                    std::string _tag_name,
                    std::string _description,
                    std::string _type,
                    bool _required,
                    std::string _default_value) : parameter
                    (_name, _human_readable_name,
                    _tag_name, _description, _type, _required){

    this->default_value = _default_value;

}

topic_name::topic_name( std::string _name,
                    std::string _human_readable_name,
                    std::string _tag_name,
                    std::string _description,
                    std::string _type,
                    bool _required,
                    std::string _default_value) : string_parameter
                    (_name, _human_readable_name, _tag_name, 
                    _description, _type, _required, _default_value) {}

link_reference::link_reference( std::string _name,
                    std::string _human_readable_name,
                    std::string _tag_name,
                    std::string _description,
                    std::string _type,
                    bool _required,
                    std::string _default_value) : string_parameter
                    (_name, _human_readable_name, _tag_name, 
                    _description, _type, _required, _default_value) {}

joint_reference::joint_reference( std::string _name,
                    std::string _human_readable_name,
                    std::string _tag_name,
                    std::string _description,
                    std::string _type,
                    bool _required,
                    std::string _default_value) : string_parameter
                    (_name, _human_readable_name, _tag_name, 
                    _description, _type, _required, _default_value) {}

model_reference::model_reference( std::string _name,
                    std::string _human_readable_name,
                    std::string _tag_name,
                    std::string _description,
                    std::string _type,
                    bool _required,
                    std::string _default_value) : string_parameter
                    (_name, _human_readable_name, _tag_name, 
                    _description, _type, _required, _default_value) {}

double_parameter::double_parameter(  std::string _name,
                    std::string _human_readable_name,
                    std::string _tag_name,
                    std::string _description,
                    std::string _type,
                    bool _required,
                    double _default_value) : parameter
                    (_name, _human_readable_name, _tag_name, 
                    _description, _type, _required) {

    this->default_value = _default_value;
}

integer_parameter::integer_parameter(  std::string _name,
                    std::string _human_readable_name,
                    std::string _tag_name,
                    std::string _description,
                    std::string _type,
                    bool _required,
                    int _default_value) : parameter
                    (_name, _human_readable_name, _tag_name,
                     _description, _type, _required) {

    this->default_value = _default_value;
}

// -------------------- end of constructors -----------------------