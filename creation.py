import dtlpy as dl
import subprocess

project = dl.projects.get(project_name='MyProject')

# Publish dpk to the Marketplace
dpk = project.dpks.publish(manifest_filepath='dataloop.json')

try:
    # Update app in project
    app = project.apps.get(app_name='opencv-face-detection')
    app.dpk_version = dpk.version
    app.update()

except dl.exceptions.NotFound:
    # Install app in project
    project.apps.install(dpk=dpk)
