
let selectAllOptions = function(input_name) {
    let checkboxes = $("input[name='" + input_name + "']:checkbox");
    let checkedboxes = $("input[name='" + input_name + "']:checkbox:checked");
    
    console.debug("checkbox ", checkboxes, ", checked ", checkedboxes);
    if(checkedboxes.length == checkboxes.length) {
        console.debug("remove checked");
        checkboxes.prop("checked", false);
    } else {
        console.debug("check all");
        checkboxes.prop('checked', "checked");
    }
};


let searchPrompts = function(inputId, q) {
    console.debug("modal shown ", inputId);
    let modalId = inputId + "OptionsSearchBox";
    let table = $("#" + modalId).find("table");
    let modalTips = $("#" + modalId).find("#modal-tips");
    let checkboxes = $("input[name='" + inputId + "']:checkbox:checked");
    console.debug("checkboxes ", checkboxes);
    let promptChecked = {};
    //from checkbox
    for(const cb of checkboxes) {
        const prompt = $(cb).prop("value");
        const checked = $(cb).prop("checked");
        promptChecked[prompt] = checked;
    }

    console.debug("promptChecked ", promptChecked);
    
    $.ajax({
        url: "/search/",
        type: "POST",
        data: JSON.stringify({category: inputId, q: q}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(resp) {
            console.debug("search done ", resp);
            //append header
            let header = [
                "<tr>",
                " <th></th>",
                " <th>Prompt</th>",
                " <th>Info</th>",
                " <th>Category</th>",
                " <th>Hit</th>",
                " <th>Hit Percentage</th>",
                "</tr>"
            ].join("");
            table.html(header);

            for(const element of resp.data) {
                let checked = "checked=checked";
                if (promptChecked[element.name] == null) {
                    checked = "";
                }
                let hit = "";
                if(element.hit > 0) {
                    hit = element.hit;
                }

                let percentage = "";
                if (element.percentage > 0) {
                    percentage = element.percentage + "%";
                }
                const node = [
                    "<tr>",
                    " <td>",
                    //"  <div class='form-check form-check-inline'>",
                    "    <input class='form-check-input' type='checkbox' name='" + inputId + "' value='" + element.name + "' " + checked + " />", 
                    //"  </div>",
                    " </td>",
                    " <td>",
                    "    <label class='form-check-label'>" + element.name + "</label>",
                    " </td>",
                    " <td>" + element.info + "</td>",
                    " <td>" + element.category + "</td>",
                    " <td>" + hit + "</td>",
                    " <td>" + percentage + "</td>",
                    "</tr>"
                ].join("");
                table.append(node);
            }

            modalTips.removeClass();
            modalTips.addClass("text-success text-end");
            modalTips.html("Found " + resp.n);
        },
        error: function(err) {
            console.error(err);
            modalTips.removeClass();
            modalTips.addClass("text-danger text-end");
            modalTips.html(err);
        }
    });
};


let showPromptResult = function(inputId) {
    let checkboxes = $("input[name='" + inputId + "']:checkbox:checked");
    let prompts = [];
    
    for(const cb of checkboxes) {
        const prompt = $(cb).prop("value");
        prompts.push(prompt);
    }

    $("#" + inputId + "Result").html(prompts.join(","));
};

