# TODO:
# - add docs
# - package examples

%define 	module	networkx
Summary:	High-productivity software for complex networks
Summary(pl.UTF-8):	Efektywne operacje na skompliwkoanych grafach.
Name:		python-%{module}
Version:	1.8.1
Release:	2
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/n/networkx/%{module}-%{version}.tar.gz
# Source0-md5:	b4a9e68ecd1b0164446ee432d2e20bd0
URL:		http://networkx.github.io/index.html
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python language software package for the creation, manipulation, and
study of the structure, dynamics, and functions of complex networks.

%description -l pl.UTF-8
Pakiet oprogramowania do tworzenia, manipulacji i badania struktury
dynamiki i funkcji zlozonych sieci.

%prep
%setup -q -n %{module}-%{version}

%build
%py_build

%install
rm -rf $RPM_BUILD_ROOT
%py_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
# %doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/%{module}-*.egg-info
%endif
%{_examplesdir}/%{name}-%{version}
