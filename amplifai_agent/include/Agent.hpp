#pragma once
#include <string>

class Agent {
public:
    virtual ~Agent() = default;
    virtual std::string respond(const std::string& input) = 0;
};
