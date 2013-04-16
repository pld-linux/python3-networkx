# TODO:
# Add docs
%define 	module	networkx
Summary:	High-productivity software for complex networks
Summary(pl.UTF-8):	Efektywne operacje na skompliwkoanych grafach.
Name:		python-%{module}
Version:	1.7
Release:	0.1
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/n/networkx/%{module}-%{version}.tar.gz#md5=1a73da9d571a206aa40f6ef69254f7b4
# Source0-md5:	1a73da9d571a206aa40f6ef69254f7b4
URL:		http://networkx.github.io/index.html
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
# if py_postclean is used
BuildRequires:	rpmbuild(macros) >= 1.219
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
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

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
