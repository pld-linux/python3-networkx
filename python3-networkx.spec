#
# Conditional build:
%bcond_with	doc	# Sphinx documentation, TODO: fix this
%bcond_with	tests	# unit tests

%define		module	networkx
Summary:	High-productivity software for complex networks
Summary(pl.UTF-8):	Efektywne operacje na skomplikowanych grafach
Name:		python3-%{module}
Version:	2.8.8
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/networkx/
Source0:	https://files.pythonhosted.org/packages/source/n/networkx/%{module}-%{version}.tar.gz
# Source0-md5:	22139ab5a47818fa00cbaa91eb126381
URL:		http://networkx.github.io/index.html
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools
%if %{with tests}
#BuildRequires:	python3-codecov >= 2.1
BuildRequires:	python3-matplotlib >= 3.4
BuildRequires:	python3-numpy >= 1.19
BuildRequires:	python3-pandas >= 1.3
BuildRequires:	python3-pytest >= 7.2
BuildRequires:	python3-pytest-cov >= 4.0
BuildRequires:	python3-scipy >= 1.8
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-nb2plots >= 0.6
BuildRequires:	python3-numpydoc >= 1.5
BuildRequires:	python3-pillow >= 9.2
BuildRequires:	python3-pydata-sphinx-theme >= 0.11
# from pygraphviz.scraper import PNGScraper
#BuildRequires:	python3-pygraphviz
BuildRequires:	python3-sphinx-gallery >= 0.11
BuildRequires:	python3-texext >= 0.6.6
BuildRequires:	sphinx-pdg-3 >= 5.2
%endif
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python language software package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%description -l pl.UTF-8
Pakiet oprogramowania do tworzenia, manipulacji i badania struktury
dynamiki i funkcji złożonych sieci.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation
Obsoletes:	python-networkx-apidocs == 2.5

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest networkx
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{module}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-*.egg-info
%{_examplesdir}/python3-%{module}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
