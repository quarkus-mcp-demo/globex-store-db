FROM registry.redhat.io/rhel9/postgresql-16

USER 0

COPY contrib/ /opt/app-root/src

RUN /usr/libexec/fix-permissions --read-only /opt/app-root/src

USER 26
