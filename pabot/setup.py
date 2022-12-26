from setuptools import setup, find_namespace_packages


setup(
    name='pabot',
    version='0.1',
    description='',
    url='https://github.com/StasStryzhakov/GoIT-8',
    teamlead='Стас Стрижаков',
    scrummaster='Катерина Помазунова',
    developers='Руслан, Макс Корнієв, Олександр Невський, ',
    include_package_data=True,
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['pabot = pabot.pabot:main']}
)



