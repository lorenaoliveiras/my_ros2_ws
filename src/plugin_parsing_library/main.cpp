#include "parameter.hpp"
#include "restriction.hpp"
#include "plugin_parameters.hpp"
#include <yaml-cpp/yaml.h>

int main() {
    YAML::Node example = YAML::LoadFile("example_plugin.yml");

    plugin_parameters test_plugin{}; 

    test_plugin.read_plugin(example);
}