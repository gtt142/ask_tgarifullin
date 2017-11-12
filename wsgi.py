from cgi import parse_qsl

def application(environ, start_response):
    output = '<h1>Привет, мир!</h1>'
    output=output+('Post:')
    output=output+('<form method="POST">')
    output=output+('<input type="text" name = "testPOST">')
    output=output+('<input type="submit" value="Send">')
    output=output+('</form><br><br>')
    output=output+('GET:')
    output=output+('<form method="GET">')
    output=output+('<input type="text" name = "testgGET">')
    output=output+('<input type="submit" value="Send">')
    output=output+('</form>')

    d = parse_qsl(environ['QUERY_STRING'])
    if environ['REQUEST_METHOD'] == 'POST':
        output=output+('<h1>Post  data:</h1>')
        output=output+(environ['wsgi.input'].read().decode())

    if environ['REQUEST_METHOD'] == 'GET':
        if environ['QUERY_STRING'] != '':
            output=output+('<h1>Get data:</h1>')
            for ch in d:
                output=output+' = '.join(ch)
                output=output+('<br>')

    start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])
    return ([output.encode()])
