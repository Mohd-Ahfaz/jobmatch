from django.contrib import admin

from .models import Profile, Question, Skill, UserSkill

admin.site.register(Skill)
admin.site.register(Profile)
admin.site.register(UserSkill)
admin.site.register(Question)
