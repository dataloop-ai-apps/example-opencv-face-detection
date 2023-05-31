import dtlpy as dl
import subprocess

project = dl.projects.get('Face Detection')

# bump patch version
subprocess.check_call('bumpversion patch --allow-dirty', shell=True)

# publish dpk to app store
dpk = project.dpks.publish()

try:
    # Update app in project
    app = project.apps.get(app_name='opencv-face-detection')
    app.dpk_version = dpk.version
    app.update()

except dl.exceptions.NotFound:
    # Install app in project
    project.apps.install(dpk=dpk)
