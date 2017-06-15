import cgi
from decimal import *
from google.appengine.api import users
import webapp2

MAIN_PAGE_HTML = """\
<html>
  <body>
  <h3>Random IPv6 Collision Probability Calculator</h3>    

  <p>This small app calculates the probability of multiple hosts independently picking the same IPv6 address, with a 
    configurable subnet size and number of hosts.</br>It is basically my
    <a href="http://mac-collision-probability.appspot.com/">MAC randomization collision probability</a> app with a 
    few numbers twiddled.</p>

  <p>Because of the <a href="http://en.wikipedia.org/wiki/Birthday_problem">Birthday paradox</a> the
       probability is much higher than most people (including myself) would expect, even when the many bits are randomized.</p>
</p>
   
    <form action="/calculate" method="post">
      <div><p>Subnet length: <input type="number" name="length" min="8" max="128" value="%s"><br>
              Number of hosts: <input type="number" name="stations" min="2" max="100000" value="%s"></div>
      <div><input type="submit" value="Calculate"></div>
    </form>
"""

MAIN_PAGE_FOOTER = """\
  <br>
  <hr>
  <small>Copyright &copy; 2017 - Warren Kumari (warren@kumari.net) v0.1</small>
  </body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML % (64, 2000))
        self.response.write(MAIN_PAGE_FOOTER)
        

class Probability(webapp2.RequestHandler):
    def get(self):
      length = self.request.get('length') or 64
      stations = Decimal(self.request.get('hosts') or 1000)
      self.response.write(MAIN_PAGE_HTML % (length, stations))
      self.response.write(MAIN_PAGE_FOOTER)
      
    def post(self):
      getcontext().prec = 64
      try:
        length = int(self.request.get('length'))
        bits = Decimal(128 - length)
        stations = Decimal(int(self.request.get('stations')))
      except ValueError, e:
        self.response.write('<head><meta http-equiv="refresh" content="0;URL=\'/\'" /></head>')
        return        
      upper = (stations * (stations - Decimal(1)))/Decimal(2)
      num = Decimal(2)**bits
      res = (num-Decimal(1))/num
      prob = Decimal(1) - res **upper
      tot = Decimal(1)/prob 
        
                 
      self.response.write(MAIN_PAGE_HTML % (length, stations))
      self.response.write('<p>The probability of a collision is : <tt>%1.32f</tt>' % prob)
      self.response.write("<br>That's 1 out of <tt>%10.2f</tt></p>" % tot)
      self.response.write(MAIN_PAGE_FOOTER)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/calculate', Probability),
], debug=False)
