var page = require('webpage').create(),
system = require('system'),
    address, output, size, csrf_token, session_id;

address = system.args[1];
output = system.args[2];
session_id = system.args[3];
url_domain = system.args[4];

phantom.addCookie({'domain': url_domain, 'name':'sessionid', 'value': session_id});

page.viewportSize = { width: 1170, height: 600 };
page.paperSize = { format: 'A4', orientation: 'portrait', margin: '1cm' };

page.open(address, function (status) {
    if (status !== 'success') {
        console.log('Unable to load the address!');
        phantom.exit();
    } else {
        page.render(output);
        phantom.exit();
    }
});
