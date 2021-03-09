#
# Conditional build:
%bcond_with	doc	# Sphinx documentation, TODO: fix this

%define		module	networkx
Summary:	High-productivity software for complex networks
Summary(pl.UTF-8):	Efektywne operacje na skompliwkoanych grafach.
Name:		python-%{module}
Version:	2.5
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/n/networkx/%{module}-%{version}.tar.gz
# Source0-md5:	21f25be1f4373e19153a9beca63346e7
URL:		http://networkx.github.io/index.html
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%{?with_doc:BuildRequires:	python3-matplotlib}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python language software package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%description -l pl.UTF-8
Pakiet oprogramowania do tworzenia, manipulacji i badania struktury
dynamiki i funkcji zlozonych sieci.

%package -n python3-%{module}
Summary:	High-productivity software for complex networks
Summary(pl.UTF-8):	Efektywne operacje na skompliwkoanych grafach.
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
Python language software package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%description -n python3-%{module} -l pl.UTF-8
Pakiet oprogramowania do tworzenia, manipulacji i badania struktury
dynamiki i funkcji zlozonych sieci.

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
%py3_build

%if %{with doc}
cd doc
%{__make} -j1 html
rm -rf _build/html/_sources
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

%files -n python3-%{module}
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
