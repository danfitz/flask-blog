from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FileField, TextAreaField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me", default=True)
    submit = SubmitField("Log In")

class PublishForm(FlaskForm):
    published = BooleanField("Publish?", default=True)
    update_timestamp = BooleanField("Update Timestamp?")
    featured_img = FileField("Featured Image")
    title = StringField("Title", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    category = SelectField(
        "Category",
        choices=[
            ("journal", "Journal"),
            ("first-world-problems", "First World Problems"),
            ("self-actualization", "Self-actualization"),
            ("relationships", "Relationships")
        ]
    )
    excerpt = PageDownField("Excerpt", validators=[DataRequired()])
    content = PageDownField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")
