from random import shuffle
from uuid import uuid4
import re
import yaml

class Challenge(object):
    def __init__(self, load_path):
        self.required = {'title': None, 'id': None, 'type': None, 'decimal': None}
        self.parameters = {}
        extension = load_path.split('.')[-1].lower()
        if extension == 'yaml':
            self._load_from_yaml(load_path)
        elif extension == 'md':
            self._load_from_markdown(load_path)

    def _construct_challenge(self):
        challenge = "### !challenge\n"
        formatter = '### !{section}\n{content}\n### !end-{section}\n'
        r_formatter = '* {section}: {content}\n'
        for section, content in self.required.iteritems():
            if content is None:
                continue
            challenge += r_formatter.format(section=section, content=content)
        for section, content in self.parameters.iteritems():
            if 'hint' in section:
                section = 'hint'
            challenge += formatter.format(section=section, content=content)
        challenge += "### !end-challenge"
        self.challenge = challenge

    def _load_from_markdown(self, load_path):
        with open(load_path, 'r') as f:
            self._process_markdown(f)

    def _load_from_yaml(self, load_path):
        with open(load_path, 'r') as f:
            self._process_yaml(yaml.load(f))

    def _process_yaml(self, yaml_dict):
        processed_dict = {}
        for k, v in yaml_dict.iteritems():
            if k.lower() in self.required:
                self.required[k.lower()] = v
            else:
                self.parameters[k.lower()] = v
        if 'options' in self.parameters:
            self._shuffle_options()

    def _process_markdown(self, f):
        challenge_start = re.compile(r'(#+?)\s+!challenge')
        challenge_end = re.compile(r'(#+?)\s+!end-challenge')
        starter = re.compile(r'(#+?)\s+!(\w+)\s')
        ender = re.compile(r'(#+?)\s+!\w+-(\w+)\s')
        for line in f:
            check_start = starter.search(line)
            check_end = ender.search(line)
            if check_start:
                print check_start.groups()
            if check_end:
                print check_end.groups()

    def _shuffle_options(self):
        temp = self.parameters['options'].split('\n')
        shuffle(temp)
        self.parameters['options'] = '\n'.join(temp)


if __name__ == '__main__':

    # file_names = ['test_challenge_mc.yaml', 'test_challenge_num.yaml']
    # for f_name in file_names:
    #     c = Challenge(f_name)
    #     c._construct_challenge()
    #     o_name = f_name.strip('yaml') + 'md'
    #     with open(o_name, 'w') as f:
    #         f.write(c.challenge)

    c = Challenge('test_challenge.md')

