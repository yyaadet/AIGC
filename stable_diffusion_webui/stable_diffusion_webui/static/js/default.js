

function render_image(item) {
    let itemHtml = [
        '<div class="col-4">',
        '  <div class="card">',
        '    <a target="_blank" href="' + item.url + '"><img src="' + item.url + '" class="card-img-top" alt="' + item.text + '" /></a>',
        '    <div class="card-body">',
        '      <p class="card-text">' + item.text + "</p>",
        '    </div>',
        '  </div>',
        '</div>'
    ].join("");

    return itemHtml;
}