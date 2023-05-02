%global qt_version 5.15.9

Summary: Qt5 - WebSockets component
Name: opt-qt5-qtwebsockets
Version: 5.15.9+kde2
Release: 1%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
Source0: %{name}-%{version}.tar.bz2

# filter qml provides
%global __provides_exclude_from ^%{_opt_qt5_archdatadir}/qml/.*\\.so$

%{?opt_qt5_default_filter}

BuildRequires: make
BuildRequires: opt-qt5-qtbase-devel >= %{qt_version}
BuildRequires: opt-qt5-qtbase-private-devel
#libQt5Core.so.5(Qt_5_PRIVATE_API)(64bit)
%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}
BuildRequires: opt-qt5-qtdeclarative-devel

%description
The QtWebSockets module implements the WebSocket protocol as specified in RFC
6455. It solely depends on Qt (no external dependencies).

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: opt-qt5-qtbase-devel%{?_isa}
Requires: opt-qt5-qtdeclarative >= %{qt_version}

%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{version}/upstream -p1


%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

%{opt_qmake_qt5}

%make_build


%install
make install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_opt_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.*
%{_opt_qt5_libdir}/libQt5WebSockets.so.5*
%{_opt_qt5_archdatadir}/qml/Qt/WebSockets/

%files devel
%{_opt_qt5_headerdir}/QtWebSockets/
%{_opt_qt5_libdir}/libQt5WebSockets.so
%{_opt_qt5_libdir}/libQt5WebSockets.prl
%dir %{_opt_qt5_libdir}/cmake/Qt5WebSockets/
%{_opt_qt5_libdir}/cmake/Qt5WebSockets/Qt5WebSocketsConfig*.cmake
%{_opt_qt5_libdir}/pkgconfig/Qt5WebSockets.pc
%{_opt_qt5_libdir}/qt5/qml/QtWebSockets/
%{_opt_qt5_archdatadir}/mkspecs/modules/qt_lib_websockets*.pri
