# vim:ts=4 sw=4 et:
class wagtail::site::staging::{{ project_name }}wagtail inherits wagtail::site::staging {
    wagtail::app { '{{ project_name }}wagtail':
        ip               => $ipaddress,
        ip6              => $ipaddress6,
        manage_ip        => false,
        manage_db        => true,
        manage_user      => true,
        appsubdir        => '{{ project_name }}',
        settings         => '{{ project_name }}/settings',
        wsgi_module      => '{{ project_name }}.wsgi',
        requirements     => 'requirements.txt',
        servername       => '{{ project_name }}-staging.torchboxapps.com',
        alias_redirect   => false,
        codebase_project => '', # CHANGEME
        codebase_repo    => '', # CHANGEME
        git_uri          => 'CODEBASE',
        django_version   => '1.7',
        staticdir        => "static",
        mediadir         => "media",
        deploy           => [ '@admin', '@wagtail' ], # CHANGEME
        python_version   => '2.7-local',
        pg_version       => '9.4',
        manade_daemons   => [
            'celery worker -C -c1 -A {{ project_name }}',
            'celery beat -A {{ project_name }} -C -s $TMPDIR/celerybeat.db --pidfile=',
        ],
        admins           => {
            # CHANGEME
            # List of users to send error emails to. Eg:
            # 'Joe Bloggs' => 'joe.bloggs@torchbox.com',
        },
        nagios_url       => '/',
        auth => {
            enabled       => true,
            hosts         => [ 'tbx' ],
            users         => {
                # CHANGEME
                # This is the credentials for HTTP authentication. Eg:
                # 'username'  => 'password',
            },
        },
    }
}
