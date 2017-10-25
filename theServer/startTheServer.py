from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.renderers import render_to_response as render
from pyramid.view import view_config

def hello_world(request):
    #return Response('Hello %(name)s!' % request.matchdict)
    return render('./templates/drums/index.mako',
                              {'foo':1, 'bar':2},
                              request=request)
#@view_config(renderer='templates/drums/index.mako')
@view_config(route_name='index')
def index(request):
    # Return a rendered template
    return Response('fred')
    # or, return a string
    #return 'Hello World'
def search(self):
    #rltString = json.dumps({"successful": True, "urlNew": "http://autumn.ims.uwm.edu:5000/paintweb/images/StemCells1.png"})
    #print rltString
    #print 'hello'
    #print request.params
    #return rltString
    return render('/drums/gene_list.mako')
def adv(self):
    return render('/drums/adv_search.mako')
def details(self):
    return render('/drums/mutation_details.mako')
def flat(self):
    return render('/drums/flat_muts.mako')
def digest(self):
    return render('/drums/digest.mako')


if __name__ == '__main__':
    config = Configurator()
    config.include('pyramid_mako')
    config.add_route('hello', '/hello/{name}')
    config.add_view(hello_world, route_name='hello')
    config.add_route('static','/')
    config.add_static_view(name='static', path='/static')
    app = config.make_wsgi_app()
    
    server = make_server('0.0.0.0', 1024, app)
    server.serve_forever()
    
    
    
