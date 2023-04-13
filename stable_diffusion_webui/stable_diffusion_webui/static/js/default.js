
let selectAllOptions = function(input_name) {
    let checkboxes = $("input[name='" + input_name + "']:checkbox");
    console.debug("checkboxes ", checkboxes);
    checkboxes.prop('checked', "checked");
};