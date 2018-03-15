from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FileField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me", default=True)
    submit = SubmitField("Log In")

class NewPostForm(FlaskForm):
    published = BooleanField("Publish?")
    title = StringField("Title", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    category = SelectField(
        "Category",
        choices=[("journal", "Journal"), ("first-world-problems", "First World Problems"), ("self-actualization", "Self-actualization"), ("relationships", "Relationships")]
    )
    featured_img = FileField("Featured Image")
    excerpt = TextAreaField("Excerpt", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")
