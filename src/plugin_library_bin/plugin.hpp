#ifndef PLUGIN_H
#define PLUGIN_H
#include <string>
#include <string.h>
#include <iostream>
#include <vector>
#include "parameter.hpp"
#include <yaml-cpp/yaml.h>

class plugin {
    public:

    std::string name;
    std::string description;
    std::string lib_name;
    std::string target;
    std::string type;
    std::string version;
    std::vector <parameter> plugin_parameters;


    plugin::plugin();

    plugin::plugin( std::string _name,
                    std::string _description,
                    std::string _lib_name,
                    std::string _target,
                    std::string _type,
                    std::string _version);

    plugin plugin::read_plugin(YAML::Node);

    parameter plugin::read_parameter(YAML::Node);

    void plugin::add_parameter(parameter);
};

#endif