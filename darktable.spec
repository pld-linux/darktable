Summary:	darktable is a virtual lighttable and darkroom for photographers
Summary(pl.UTF-8):	darktable to wirtualny podświetlany stół i ciemnia dla fotografów
Name:		darktable
Version:	0.6
Release:	2
License:	GPL v3
Group:		X11/Applications/Graphics
Source0:	http://downloads.sourceforge.net/darktable/%{name}-%{version}.tar.gz
# Source0-md5:	64a0c4ba2000605137ba2e57434ee3fe
URL:		http://darktable.sourceforge.net/
BuildRequires:	GConf2-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	curl-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	exiv2-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel
BuildRequires:	intltool
BuildRequires:	lcms-devel
BuildRequires:	lensfun-devel
BuildRequires:	libglade2-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libgomp-devel
BuildRequires:	libgphoto2-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libtiff-devel
BuildRequires:	pkgconfig
BuildRequires:	sqlite3-devel
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
darktable is a virtual lighttable and darkroom for photographers

%description -l pl.UTF-8
darktable to wirtualny podświetlany stół i ciemnia dla fotografów

%prep
%setup -q

%build

%configure \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_icon_cache hicolor
%gconf_schema_install:

%postun
%update_desktop_database_postun
%update_icon_cache hicolor
%gconf_schema_uninstall

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root)  %{_bindir}/darktable
%{_datadir}/darktable
%{_desktopdir}/darktable.desktop
%{_iconsdir}/hicolor/*/apps/darktable.png
%{_iconsdir}/hicolor/scalable/apps/darktable.svg
%dir %{_libdir}/darktable
%dir %{_libdir}/darktable/plugins
%dir %{_libdir}/darktable/plugins/imageio
%dir %{_libdir}/darktable/plugins/imageio/format
%dir %{_libdir}/darktable/plugins/imageio/storage
%dir %{_libdir}/darktable/plugins/lighttable
%dir %{_libdir}/darktable/views
%attr(755,root,root) %{_libdir}/darktable/libdarktable.so
%attr(755,root,root) %{_libdir}/darktable/plugins/*.so
%attr(755,root,root) %{_libdir}/darktable/plugins/imageio/format/*.so
%attr(755,root,root) %{_libdir}/darktable/plugins/imageio/storage/*.so
%attr(755,root,root) %{_libdir}/darktable/plugins/lighttable/*.so
%attr(755,root,root) %{_libdir}/darktable/views/*.so
%{_mandir}/man1/darktable.*
%{_sysconfdir}/gconf/schemas/darktable.schemas
