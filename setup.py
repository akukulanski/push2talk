from setuptools import setup, find_packages


def install_requires():
    with open('./requirements.txt', 'r') as f:
        return [line.replace('\n', '') for line in f.readlines()]


def long_description():
    with open("readme.md") as f:
        return f.read()


setup(name='push2talk',
      version='0.0.1',
      author='Ariel Kukulanski',
      author_email='akukulanski@gmail.com',
      description='Push to talk.',
      long_description=long_description(),
      long_description_content_type='text/markdown',
      packages=find_packages(),
      license='BSD',
      python_requires="~=3.6",
      url='https://github.com/akukulanski/push2talk',
      # download_url=,
      keywords=['pushtotalk'],
      setup_requires=['setuptools_scm', 'wheel'],
      install_requires=install_requires(),
      include_package_data=True,
      entry_points={'console_scripts': [
                        'push2talk=push2talk.push2talk:main']},
      project_urls={
          "Source Code": "https://github.com/akukulanski/push2talk",
          "Bug Tracker": "https://github.com/akukulanski/push2talk/issues",
      },
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Topic :: Utilities'])
