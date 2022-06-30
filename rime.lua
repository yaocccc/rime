-- 已词定字 例: 已有候选项 "你好" 则 "[ 输入你" "] 输入好"
select_character_processor = require("select_character")

-- 输入特定短语转换成需要的候选
translator = require("translator")
