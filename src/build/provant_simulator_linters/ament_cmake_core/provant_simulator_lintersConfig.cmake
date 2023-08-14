# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_provant_simulator_linters_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED provant_simulator_linters_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(provant_simulator_linters_FOUND FALSE)
  elseif(NOT provant_simulator_linters_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(provant_simulator_linters_FOUND FALSE)
  endif()
  return()
endif()
set(_provant_simulator_linters_CONFIG_INCLUDED TRUE)

# output package information
if(NOT provant_simulator_linters_FIND_QUIETLY)
  message(STATUS "Found provant_simulator_linters: 0.1.0 (${provant_simulator_linters_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'provant_simulator_linters' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${provant_simulator_linters_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(provant_simulator_linters_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "ament_cmake_export_dependencies-extras.cmake")
foreach(_extra ${_extras})
  include("${provant_simulator_linters_DIR}/${_extra}")
endforeach()
