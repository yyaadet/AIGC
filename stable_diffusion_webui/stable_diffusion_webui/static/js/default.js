

function render_image() {
    let itemHtml = [
        '<div class="col-4">',
        '  <div class="card">',
        '    <img src="' + item.url + '" class="card-img-top" alt="' + item.text + '" />',
        '    <div class="card-body">',
        '      <p class="card-text">' + item.text + "</p>",
        '    </div>',
        '  </div>',
        '</div>'
    ].join("");

    return itemHtml;
}