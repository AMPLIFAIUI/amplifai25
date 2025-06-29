#pragma once
#include <string>
#include <vector>

class ModelEnsemble {
public:
    void add_model(const std::string& model_name);
    std::string select_model(const std::string& task_type) const;
private:
    std::vector<std::string> models_;
};
