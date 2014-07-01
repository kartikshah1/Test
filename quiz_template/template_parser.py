"""Template Parser"""
import ConfigParser
import os
import unittests


class TemplateParser:
    """Class to parse quiz templates
    """
    def __init__(self, template_file):
        self.template = ConfigParser.ConfigParser()
        self.template.read(template_file)

    def get_all_sections(self):
        return self.templates.sections()

    def get_question_map(self, question_tag):
        question_map = {}
        details = self.template.options(question_tag)
        for sub_tag in details:
            try:
                question_map[sub_tag] = self.template.get(question_tag,
                                                          sub_tag)
                if question_map[sub_tag] == -1:
                    raise ValueError("Question sub tags not found")
            except Exception as ex:
                print "Exception %s on %s" % (ex, sub_tag)
                question_map[sub_tag] = None
        return question_map

    def club_question_with_subparts(self, question_list):
        pass

    def template_reader(self):
        all_sections = self.get_all_sections()
        assert len(all_sections) is not 0
        for question in all_sections:
            pass
