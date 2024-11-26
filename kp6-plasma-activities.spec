#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeplasmaver	6.2.4
%define		qt_ver		6.7.0
%define		kf_ver		6.5.0
%define		kpname		plasma-activities

Summary:	Plasma KActivities components
Summary(pl.UTF-8):	Komponenty Plazmy KActivities
Name:		kp6-%{kpname}
Version:	6.2.4
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	e5f30475eedf219b7b2018ea47f82789
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qt_ver}
BuildRequires:	Qt6DBus-devel >= %{qt_ver}
BuildRequires:	Qt6Gui-devel >= %{qt_ver}
BuildRequires:	Qt6Qml-devel >= %{qt_ver}
BuildRequires:	Qt6Quick-devel >= %{qt_ver}
BuildRequires:	Qt6Sql-devel >= %{qt_ver}
BuildRequires:	Qt6Widgets-devel >= %{qt_ver}
BuildRequires:	boost-devel >= 1.49
BuildRequires:	cmake >= 3.16.0
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kf_ver}
BuildRequires:	kf6-kconfig-devel >= %{kf_ver}
BuildRequires:	kf6-kcoreaddons-devel >= %{kf_ver}
# C++20
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	xz
Obsoletes:	kp5-plasma-activities < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Core components for the KDE Activity concept.

%description -l pl.UTF-8
Główne komponenty idei KDE Activity.

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Core-devel >= %{qt_ver}
Requires:	libstdc++-devel >= 6:8
Obsoletes:	kp5-plasma-activities < 6

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}

%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/plasma-activities-cli6
%attr(755,root,root) %{_libdir}/libPlasmaActivities.so.*.*
%ghost %{_libdir}/libPlasmaActivities.so.6
%dir %{_libdir}/qt6/qml/org/kde/activities
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/activities/libplasmaactivitiesextensionplugin.so
%{_libdir}/qt6/qml/org/kde/activities/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/activities/plasmaactivitiesextensionplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/activities/qmldir
%{_datadir}/qlogging-categories6/plasma-activities.categories
%{_datadir}/qlogging-categories6/plasma-activities.renamecategories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libPlasmaActivities.so
%{_includedir}/PlasmaActivities
%{_libdir}/cmake/PlasmaActivities
%{_pkgconfigdir}/PlasmaActivities.pc
