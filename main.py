import webapp2
import os
from google.appengine.ext.webapp import template
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


class MainPage(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/signup.html')
        self.response.out.write(template.render(path, {"message": "Please enter your details"}))

    def post(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/signup.html')
        have_error = False
        username_input = self.request.get("username")
        password_input = self.request.get("password")
        verify_input = self.request.get("verify")
        email_input = self.request.get("email")

        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""

        if not valid_username(username_input):
            username_error = "This is not a valid username!"
            username_input = ""
            have_error = True

        if not valid_password(password_input):
            password_error = "This is not a valid password!"
            have_error = True
        elif password_input != verify_input:
            verify_error = "Passwords did not match"
            have_error = True

        if not valid_email(email_input):
            email_error = "This is not a valid email"
            email_input = ""
            have_error = True
    
        if have_error:
            self.response.out.write(template.render(path, {
                "message": "Please correct mistakes", 
                "username_error": username_error,
                "password_error": password_error,
                "verify_error": verify_error,
                "email_error": email_error,
                "username_value": username_input,
                "email_value": email_input
                }))
        else:
            self.redirect("/welcome?username=" + username_input)

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/welcome.html')
        username = self.request.get("username") 
        if valid_username(username):
            self.response.out.write(template.render(path, {"username": username}))
        else:
            self.redirect("/")
        

app = webapp2.WSGIApplication([('/', MainPage), ('/welcome', WelcomePage)], debug=True)
