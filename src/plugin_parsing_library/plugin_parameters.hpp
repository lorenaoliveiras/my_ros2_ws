#include <string>
#include <string.h>
#include <iostream>
#include <vector>
#include "parameter.hpp"
#include <yaml-cpp/yaml.h>

class plugin_parameters {

    public:

        std::vector <parameter> parameters;

        plugin_parameters();

        void read_plugin(YAML::Node);

        parameter read_parameter(YAML::Node);

};