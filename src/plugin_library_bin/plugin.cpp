#include <yaml-cpp/yaml.h>
#include "plugin.hpp"

plugin::plugin() {}

plugin::plugin( std::string _name,
                std::string _description,
                std::string _lib_name,
                std::string _target,
                std::string _type,
                std::string _version) 
{
    this->name = _name;
    this->description= _description;
    this->lib_name = _lib_name;
    this->target = _target;
    this->type = _type;
    this->version = _version;
} 

plugin plugin::read_plugin(YAML::Node _config)
{
    std::string plugin_name        = _config["name"].as<std::string>();
    std::string plugin_description = _config["description"].as<std::string>();
    std::string plugin_lib_name    = _config["lib_name"].as<std::string>();
    std::string plugin_target      = _config["target"].as<std::string>();
    std::string plugin_type        = _config["type"].as<std::string>();
    std::string plugin_version     = _config["version"].as<std::string>();

    plugin Plugin(  plugin_name, plugin_description, plugin_lib_name, plugin_target,
                    plugin_type, plugin_version);

    return Plugin;

}

parameter plugin::read_parameter(YAML::Node _config) {

    std::string parameter_name = _config["name"].as<std::string>();
    std::string parameter_human_readable_name = _config["human_readable_name"].as<std::string>();
    std::string parameter_tag_name = _config["tag_name"].as<std::string>();
    std::string parameter_description = _config["description"].as<std::string>();
    std::string parameter_type = _config["type"].as<std::string>();
    bool parameter_required = _config["required"].as<bool>();

    if (parameter_type == "string") {

        std::string parameter_default;

        if (_config["default"]) {
            parameter_default = _config["default"].as<std::string>();
        }
        else {
            parameter_default = "no default value";
        }

        string_parameter StringParameter(   parameter_name, parameter_human_readable_name,
                                            parameter_tag_name, parameter_description,
                                            parameter_type, parameter_required, parameter_default);

        return StringParameter;
    } 
    else if (parameter_type == "topic_name") {
        
        std::string parameter_default;

        if (_config["default"]) {
            parameter_default = _config["default"].as<std::string>();
        }
        else {
            parameter_default = "no default value";
        }

        topic_name TopicName(   parameter_name, parameter_human_readable_name,
                                parameter_tag_name, parameter_description,
                                parameter_type, parameter_required, parameter_default);

        return TopicName;

    }
    else if (parameter_type == "link_ref") {
        std::string parameter_default;

        if (_config["default"]) {
            parameter_default = _config["default"].as<std::string>();
        }
        else {
            parameter_default = "no default value";
        }

        link_reference LinkRef( parameter_name, parameter_human_readable_name,
                                parameter_tag_name, parameter_description,
                                parameter_type, parameter_required, parameter_default);

        return LinkRef;
    }
    else if (parameter_type == "joint_ref") {
        std::string parameter_default;

        if (_config["default"]) {
            parameter_default = _config["default"].as<std::string>();
        }
        else {
            parameter_default = "no default value";
        }

        joint_reference JointRef(   parameter_name, parameter_human_readable_name,
                                    parameter_tag_name, parameter_description,
                                    parameter_type, parameter_required, parameter_default);

        return JointRef;
    }
    else if (parameter_type == "model_ref") {
        std::string parameter_default;

        if (_config["default"]) {
            parameter_default = _config["default"].as<std::string>();
        }
        else {
            parameter_default = "no default value";
        }

        model_reference ModelRef(   parameter_name, parameter_human_readable_name,
                                parameter_tag_name, parameter_description,
                                parameter_type, parameter_required, parameter_default);

        return ModelRef;
    }
    else if (parameter_type == "double") {
        double parameter_default;

        if (_config["default"]) {
            parameter_default = _config["default"].as<double>();
        }
        else {
            parameter_default = -1.0;
        }

        integer_parameter IntParameter( parameter_name, parameter_human_readable_name,
                                        parameter_tag_name, parameter_description,
                                        parameter_type, parameter_required, parameter_default);

        return IntParameter;
    }
    else if (parameter_type == "int") {
        int parameter_default;

        if (_config["default"]) {
            parameter_default = _config["default"].as<int>();
        }
        else {
            parameter_default = -1;
        }

        double_parameter DoubleParameter(   parameter_name, parameter_human_readable_name,
                                            parameter_tag_name, parameter_description,
                                            parameter_type, parameter_required, parameter_default);

        return DoubleParameter;
    }

}

void plugin::add_parameter(parameter _parameter) {
    this->plugin_parameters.push_back(_parameter);
}