#pragma once
#include <stdexcept>

class AmplifaiException : public std::runtime_error {
public:
    explicit AmplifaiException(const std::string& msg) : std::runtime_error(msg) {}
};
