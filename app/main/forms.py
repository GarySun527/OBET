#################################
# Form definitions as classes 
#################################


# Import the Form class, fields, and validators from wtform
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, FieldList, IntegerField, SelectField, SelectMultipleField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required, Length, Optional, Email, Regexp, NumberRange, URL
from wtforms import ValidationError
from wtforms import widgets
#from flask.ext.pagedown.fields import PageDownField

# Import database models
from ..models import User, Lit, Role

# Search form for index.html (main page)
class SearchFormMain(Form):
    # Search by
    search = StringField('Enter some terms to search on separated by a space:', validators = [Required()])
    # Submit button
    submit = SubmitField('Search')
    
# Search form for regular search
class SearchForm(Form):
	search = StringField('Enter some terms to search on separated by a space:', validators = [Required()])
        sort = SelectField('Sort by: ', choices = [('None',''), ('author', 'Author/Editor'), ('created_date', 'Date Created'), ('creator', 'Creator'), ('primaryField', 'Primary Field'), ('title', 'Title')])
        submit = SubmitField('Search')
    
# Not currently being used
# Advanced search
class AdvancedSearchForm(Form):
    	refType = SelectField('Reference Type', choices=[('Book Section','Book Section'), ('Edited Book', 'Edited Book') , ('Journal Article', 'Journal Article'), ('Journal Issue', 'Journal Issue'),
        ('Magazine Article', 'Magazine Article'), ('Media', 'Media'), ('Newspaper Article', 'Newspaper Article'), ('Report', 'Report'), ('Thesis', 'Thesis'), ('Website', 'Website')], default = None)
	title = StringField('Title', default = None)
	author = StringField('Author', default = None)
    	submit = SubmitField('Search')
    	
# For for privileged users to add material into the database
class AddLitForm(Form):
    refType = SelectField('Reference Type', validators = [Required()], choices=[('Book Section','Book Section'), ('Edited Book', 'Edited Book') , ('Journal Article', 'Journal Article'), ('Journal Issue', 'Journal Issue'),('Magazine Article', 'Magazine Article'), ('Media', 'Media'), ('Newspaper Article', 'Newspaper Article'), ('Report', 'Report'), ('Thesis', 'Thesis'), ('Website', 'Website')])
    author = StringField('Author', validators = [Length(0,120)])
    title = StringField('Title', validators = [Required(), Length(1,150)])
    yrPublished = IntegerField('Year Published', validators = [NumberRange(min=1800), Optional()])  # MUST ADD max_value!!! Limit it to THIS year!!
    sourceTitle = StringField('SourceTitle', validators = [Length(0,200)])
    editor = StringField('Editor', validators = [Length(0,150)])
    placePublished = StringField('Place Published', validators = [Length(0,150)])
    publisher = StringField('Publisher', validators = [Length(0,200)])
    volume = StringField('Volume', validators = [Length(0,150)])
    number = StringField('Number', validators = [Length(0,100)])
    pages = StringField('Pages', validators = [Length(0,200)])
    keywords = StringField('Keywords', validators = [Length(0,250)])
    abstract = TextAreaField('Abstract', validators = [Length(0,2000)])
    notes = TextAreaField('Notes', validators = [Length(0,500)])
    primaryField = SelectField('Primary Field', validators = [Required()], choices = [('Philosophy/Ethics/Theology','Philosophy/Ethics/Theology'), ('Anthropology/Psychology/Sociology','Anthropology/Psychology/Sociology'), ('History/Politics/Law','History/Politics/Law'), ('Agriculture/Energy/Industry','Agriculture/Energy/Industry'), ('Animal Science/Welfare','Animal Science/Welfare'), ('Ecology/Conservation','Ecology/Conservation'), ('Nature Writing/Art/Literary Criticism','Nature Writing/Art/Literary Criticism'), ('Education/Living','Education/Living')]) 
    secondaryField = SelectField('Secondary Field', choices = [('','None'), ('Philosophy/Ethics/Theology','Philosophy/Ethics/Theology'), ('Anthropology/Psychology/Sociology','Anthropology/Psychology/Sociology'), ('History/Politics/Law','History/Politics/Law'), ('Agriculture/Energy/Industry','Agriculture/Energy/Industry'), ('Animal Science/Welfare','Animal Science/Welfare'), ('Ecology/Conservation','Ecology/Conservation'), ('Nature Writing/Art/Literary Criticism','Nature Writing/Art/Literary Criticism'), ('Education/Living','Education/Living')])
    link = StringField('Link', validators = [URL(), Optional()], filters = [lambda x: x or None])
    submit = SubmitField('Submit')   
    	
# Delete user 
# Not currently being used
class DeleteUserForm(Form):
	email = EmailField("Email", validators=[Required()])
    	submit = SubmitField('Delete User')

# Delete literature 
# Not currently being used
class DeleteLitForm(Form):
	refType = SelectField('Reference Type', choices=[('Book Section','Book Section'), ('Edited Book', 'Edited Book') , ('Journal Article', 'Journal Article'), ('Journal Issue', 'Journal Issue'),
        ('Magazine Article', 'Magazine Article'), ('Media', 'Media'), ('Newspaper Article', 'Newspaper Article'), ('Report', 'Report'), ('Thesis', 'Thesis'), ('Website', 'Website')], default = None)
	title = StringField('Title', validators = [Required(), Length(1,150)])
        author = StringField('Author', validators = [Required(), Length(1,120)])
    	submit = SubmitField('Delete Lit')

# Test
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

# User preferences for search results view
# User may chose which fields to show in their search results
class Preferences(Form):
    author = BooleanField('Author')
    yrPublished = BooleanField('Year Published')
    title = BooleanField('Title')
    sourceTitle = BooleanField('Source Title')
    primaryField = BooleanField('Primary Field')
    editor = BooleanField('Editor')
    refType = BooleanField('Reference Type')
    creator = BooleanField('Creator')
    dateCreatedOn = BooleanField('Date Created')
    lastModified = BooleanField('Last Modified')
    lastModifiedBy = BooleanField('Last Modified By')
    submit = SubmitField('Update')

# Edit user profile
class EditProfileForm(Form):
    credentials = StringField('Credentials', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    description = TextAreaField('About me', validators=[Length(0, 1000)])
        #list_of_fields = ["Title", "Author", "Primary Field","Source Title", "Editor", "Year Published", "Type", "Creator", "Date Created", "Last Modified", "Last Modified By"]
        #fields = [(x, x) for x in list_of_fields]
        #searchFields = MultiCheckboxField('Search Table Fields', choices=fields)
    submit = SubmitField('Update')

# Admin profile
class EditProfileAdminForm(Form):
 	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
 	role = SelectField('Role')
 	name = StringField('Real name', validators=[Length(1, 64)])
 	location = StringField('Location', validators=[Length(0, 64)])
 	description = TextAreaField('About me', validators=[Length(0, 1000)])
 	confirmed = BooleanField('Confirmed')
 	approved = BooleanField('Approved')
 	activated = BooleanField('Activated')
        submit = SubmitField('Update')

 	def __init__(self, user, *args, **kwargs):
 		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
 		self.role.choices = [(role.name, role.name) for role in Role.objects()]
 		self.user = user
 
 	def validate_email(self, field):
 		if field.data != self.user.email and User.objects(email__iexact = field.data).first():
 			raise ValidationError('Email already registered.')
    	
