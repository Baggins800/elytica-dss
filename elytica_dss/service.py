import json
import requests
from .user import User
from .project import Project
from .application import Application
from .job import Job
from .inputfile import InputFile
from .outputfile import OutputFile

class Service:
  def __init__(self, api_key):
    self.__api_key = api_key
    self.__headers = {"Authorization": "Bearer " + api_key}
    self.__scheme = "https://"
    self.__basename = "service.elytica.com/api"
    self.__api_user = "/user" 
    self.__api_projects = "/projects" 
    self.__api_applications = "/applications" 
    self.__api_projects_createjob = "/projects/{project}/createjob" 
    self.__api_projects_getjobs = "/projects/{project}/getjobs" 
    self.__api_projects_files = "/projects/{project}/files" 
    self.__api_update = "/update/{job}" 
    self.__api_projects_upload = "/projects/{project}/upload"
    self.__api_projects_assignfile = "/projects/{project}/assignfile/{job}"
    self.__api_projects_outputfiles = "/projects/{project}/outputfiles/{job}"
    self.__api_projects_download = "/projects/{project}/download/{file}"
    self.__projects = []
    self.__jobs = []
    self.__applications = []
    self.__inputfiles = []
    self.__outputfiles = []
    self.__selected_project = None
    self.__selected_application = None
    self.__selected_job = None

  def login(self, *args, **kwargs):
    self.__api_key = kwargs.get('api_key', self.__api_key)
    self.__headers = {"Authorization": "Bearer " + self.__api_key}
    try:
      results = requests.get(\
        self.__scheme + self.__basename + self.__api_user, \
        headers=self.__headers)
      results.raise_for_status()
      self.__user = User(results.json())
    except requests.exceptions.HTTPError as err:
      raise SystemExit(err) 

  def selectProjectByName(self, name):
    self.__jobs.clear()
    self.__inputfiles.clear()
    if len(self.__projects) == 0:
      self.getProjects()
    for x in self.__projects:
      if name == x.name:
        self.__selected_project = x
        return x;

  def selectProjectById(self, id):
    self.__jobs.clear()
    self.__inputfiles.clear()
    if len(self.__projects) == 0:
      self.getProjects()
    for x in self.__projects:
      if id == x.id:
        self.__selected_project = x
        return x;

  def selectJobByName(self, name):
    if len(self.__jobs) == 0:
      self.getJobs()
    for x in self.__jobs:
      if name == x.name:
        self.__selected_job = x
        return x;

  def selectJobById(self, id):
    if len(self.__jobs) == 0:
      self.getJobs()
    for x in self.__jobs:
      if id == x.id:
        self.__selected_job = x
        return x;


  def uploadFileContents(self, filename, contents):
    try:
      results = requests.post(\
        self.__scheme + self.__basename +\
        self.__api_projects_upload.replace("{project}",\
        str(self.__selected_project.id)), \
        files={"files[]" : (filename, contents)}, \
        headers=self.__headers) 
      results.raise_for_status()
      if isinstance(results.json(), object):
        if "newfiles" not in results.json():
          raise KeyError("data does not contain a newfiles field.")
        if "oldfiles" not in results.json():
          raise KeyError("data does not contain an oldfiles field.")
        if isinstance(results.json()['oldfiles'], list):
          ifs=self.__inputfiles
          oifs=[InputFile(infile).id for infile in results.json()['oldfiles']]
          self.__inputfiles=[i for i in ifs if i.id in oifs]
        if isinstance(results.json()['newfiles'], list):
          for x in results.json()['newfiles']:
            inputFile = InputFile(x)
            self.__inputfiles.append(inputFile)
            return inputFile
      else:
        raise SystemExit('Invalid InputFile data.')
      return self.__inputfiles
    except requests.exceptions.HTTPError as err:
      raise SystemExit(err)

  def getInputFiles(self):
    try:
      results = requests.get(\
        self.__scheme + self.__basename +\
        self.__api_projects_files.replace("{project}",\
        str(self.__selected_project.id)), \
        headers=self.__headers) 
      results.raise_for_status()
      self.__inputfiles.clear()
      if isinstance(results.json(), list):
        for x in results.json():
          self.__inputfiles.append(InputFile(x))
      else:
        raise SystemExit('Invalid InputFile data.')
      return self.__inputfiles
    except requests.exceptions.HTTPError as err:
      raise SystemExit(err)

  def getOutputFiles(self):
    try:
      results = requests.get(\
        self.__scheme + self.__basename +\
        self.__api_projects_outputfiles.replace("{project}",\
        str(self.__selected_project.id)).replace("{job}",\
        str(self.__selected_job.id)), \
        headers=self.__headers) 
      results.raise_for_status()
      self.__outputfiles.clear()
      if isinstance(results.json(), list):
        for x in results.json():
          self.__outputfiles.append(OutputFile(x))
      else:
        raise SystemExit('Invalid OutputFile data.')
      return self.__outputfiles
    except requests.exceptions.HTTPError as err:
      raise SystemExit(err)

  def downloadFile(self, file):
    try:
      results = requests.get(\
        self.__scheme + self.__basename +\
        self.__api_projects_download.replace("{project}",\
        str(self.__selected_project.id)).replace("{file}",\
        str(file.id)), \
        headers=self.__headers) 
      results.raise_for_status()
      return results.content
    except requests.exceptions.HTTPError as err:
      raise SystemExit(err)

  def assignFile(self, inputfile, argument):
    try:
      data={"arg": argument, "file": inputfile.id}
      results = requests.post(\
        self.__scheme + self.__basename +\
        self.__api_projects_assignfile.replace("{project}",\
        str(self.__selected_project.id)).replace("{job}",\
        str(self.__selected_job.id)), \
        data=data,\
        headers=self.__headers) 
      results.raise_for_status()
      return results.json()
    except requests.exceptions.HTTPError as err:
      raise SystemExit(err)

  def getProjects(self):
    try:
      results = requests.get(\
        self.__scheme + self.__basename + self.__api_projects, \
        headers=self.__headers) 
      results.raise_for_status()
      self.__projects.clear()
      if isinstance(results.json(), list):
        for x in results.json():
          self.__projects.append(Project(x))
      else:
        raise SystemExit('Invalid Project data.')
      return self.__projects
    except requests.exceptions.HTTPError as err:
      raise SystemExit(err) 

  def getJobs(self):
    try:
      results = requests.get(\
        self.__scheme + self.__basename + \
        self.__api_projects_getjobs.replace("{project}",\
        str(self.__selected_project.id)), \
        headers=self.__headers) 
      results.raise_for_status()
      self.__jobs.clear()
      if isinstance(results.json(), list):
        for x in results.json():
          self.__jobs.append(Job(x))
      else:
        raise SystemExit('Invalid Job data.')
      return self.__jobs
    except requests.exceptions.HTTPError as err:
      raise SystemExit(err) 

  def createJob(self, name, priority):
    try:
      results = requests.post(\
        self.__scheme + self.__basename +\
        self.__api_projects_createjob.replace("{project}",\
        str(self.__selected_project.id)), \
        headers=self.__headers,\
        data={"name": name,\
        "priority": priority})
      results.raise_for_status()
      if isinstance(results.json(), object):
        self.__selected_job = results.json()
        self.__jobs.append(self.__selected_project) 
      else:
        raise SystemExit('Invalid Job data.')
      return self.__jobs
    except requests.exceptions.HTTPError as err:
      raise SystemExit(err)   

  def queueJob(self):
    try:
      results = requests.put(\
        self.__scheme + self.__basename +\
        self.__api_update.replace("{job}",\
        str(self.__selected_job.id)), \
        headers=self.__headers,\
        data={"updatedstatus": 1})
      results.raise_for_status()
      if isinstance(results.json(), object):
        self.__selected_job = Job(results.json())
        for x in self.__jobs:
          if x.id == self.__selected_job.id:
            x = self.__selected_job
      else:
        raise SystemExit('Invalid Job data.')
      return self.__selected_job
    except requests.exceptions.HTTPError as err:
      raise SystemExit(err)   

  def createProject(self, name, description, application):
    try:
      results = requests.post(\
        self.__scheme + self.__basename + self.__api_projects, \
        headers=self.__headers,\
        data={"name": name,\
        "description": description,\
        "application": application.id})
      results.raise_for_status()
      if isinstance(results.json(), object):
          project = Project(results.json())
          self.__projects.append(project)
          self.__selected_project = project
          self.createJob("Initial Job", 1)
      else:
        raise SystemExit('Invalid Project data.')
      return self.__projects
    except requests.exceptions.HTTPError as err:
      raise SystemExit(err)   

  def selectApplicationByName(self, name):
    if len(self.__applications) == 0:
      self.getApplications()
    for x in self.__applications:
      if name == x.display_name:
        self.__selected_application = x
        return x;

  def getApplications(self):
    try:
      results = requests.get(\
        self.__scheme + self.__basename + self.__api_applications, \
        headers=self.__headers) 
      results.raise_for_status()
      self.__applications.clear()
      if isinstance(results.json(), list):
        for x in results.json():
          self.__applications.append(Application(x))
      else:
        raise SystemExit('Invalid Application data.')
      return self.__applications
    except requests.exceptions.HTTPError as err:
      raise SystemExit(err) 
