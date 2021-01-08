from setuptools import setup

setup(
		name="stock_6",
		version="0.0.1",
		description="taiwan stock analysis",
		packages=[
			"stock_6.cmd",
			"stock_6.processor",
		],
		install_requires=[
				"requests >= 2.24.0",
				"beautifulsoup4 >= 4.9.1",
		],
		entry_points={
				'console_scripts': ['stock_6  = stock_6.cmd.main:main', ],
		},
		classifiers=[
				"Development Status :: 3 - Alpha",
				"Intended Audience :: Developers",
				"Operating System :: POSIX",
				"Programming Language :: Python :: 3.7",
		],
)

# vim: tabstop=4 shiftwidth=4
