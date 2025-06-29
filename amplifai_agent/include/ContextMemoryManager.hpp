#pragma once
#include <vector>
#include <string>

class ContextMemoryManager {
public:
    void add_context(const std::string& context);
    std::vector<std::string> get_contexts() const;
private:
    std::vector<std::string> contexts_;
};
