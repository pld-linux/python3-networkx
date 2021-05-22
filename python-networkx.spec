# TODO:
# - add docs
#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
%bcond_with	doc	# Sphinx documentation, TODO: fix this
%bcond_with	tests	# unit tests (2 failures)

%define		module	networkx
Summary:	High-productivity software for complex networks
Summary(pl.UTF-8):	Efektywne operacje na skomplikowanych grafach
Name:		python-%{module}
Version:	2.2
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/networkx/
Source0:	https://files.pythonhosted.org/packages/source/n/networkx/%{module}-%{version}.zip
# Source0-md5:	82608a3686fb3e61f20cf13bfd3c1b4a
URL:		http://networkx.github.io/index.html
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-nose >= 0.10.1
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-nose >= 0.10.1
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	unzip
%if %{with doc}
BuildRequires:	python3-nb2plots
BuildRequires:	python3-sphinx-gallery
BuildRequires:	python3-texext
BuildRequires:	sphinx-pdg-3 >= 1.3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python language software package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%description -l pl.UTF-8
Pakiet oprogramowania do tworzenia, manipulacji i badania struktury
dynamiki i funkcji złożonych sieci.

%package -n python3-%{module}
Summary:	High-productivity software for complex networks
Summary(pl.UTF-8):	Efektywne operacje na skomplikowanych grafach
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-%{module}
Python language software package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%description -n python3-%{module} -l pl.UTF-8
Pakiet oprogramowania do tworzenia, manipulacji i badania struktury
dynamiki i funkcji złożonych sieci.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python}|'
%endif

%if %{with python3}
%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{module}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS.rst LICENSE.txt README.rst
%{py_sitescriptdir}/networkx
%{py_sitescriptdir}/networkx-%{version}-py*.egg-info
%{_examplesdir}/python-%{module}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CONTRIBUTORS.rst LICENSE.txt README.rst
%{py3_sitescriptdir}/networkx
%{py3_sitescriptdir}/networkx-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
