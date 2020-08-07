# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google import auth  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore


import grpc  # type: ignore

from google.cloud.dataproc_v1.types import jobs
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import JobControllerTransport


class JobControllerGrpcTransport(JobControllerTransport):
    """gRPC backend transport for JobController.

    The JobController provides methods to manage jobs.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _stubs: Dict[str, Callable]

    def __init__(
        self,
        *,
        host: str = "dataproc.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        channel: grpc.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): The mutual TLS endpoint. If
                provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]): A
                callback to provide client SSL certificate bytes and private key
                bytes, both in PEM format. It is ignored if ``api_mtls_endpoint``
                is None.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
        elif api_mtls_endpoint:
            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            if credentials is None:
                credentials, _ = auth.default(
                    scopes=self.AUTH_SCOPES, quota_project_id=quota_project_id
                )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
            )

        self._stubs = {}  # type: Dict[str, Callable]

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
            quota_project_id=quota_project_id,
        )

    @classmethod
    def create_channel(
        cls,
        host: str = "dataproc.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs
    ) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            address (Optionsl[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            **kwargs
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = self.create_channel(
                self._host, credentials=self._credentials,
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if "operations_client" not in self.__dict__:
            self.__dict__["operations_client"] = operations_v1.OperationsClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self.__dict__["operations_client"]

    @property
    def submit_job(self) -> Callable[[jobs.SubmitJobRequest], jobs.Job]:
        r"""Return a callable for the submit job method over gRPC.

        Submits a job to a cluster.

        Returns:
            Callable[[~.SubmitJobRequest],
                    ~.Job]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "submit_job" not in self._stubs:
            self._stubs["submit_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataproc.v1.JobController/SubmitJob",
                request_serializer=jobs.SubmitJobRequest.serialize,
                response_deserializer=jobs.Job.deserialize,
            )
        return self._stubs["submit_job"]

    @property
    def submit_job_as_operation(
        self,
    ) -> Callable[[jobs.SubmitJobRequest], operations.Operation]:
        r"""Return a callable for the submit job as operation method over gRPC.

        Submits job to a cluster.

        Returns:
            Callable[[~.SubmitJobRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "submit_job_as_operation" not in self._stubs:
            self._stubs["submit_job_as_operation"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataproc.v1.JobController/SubmitJobAsOperation",
                request_serializer=jobs.SubmitJobRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["submit_job_as_operation"]

    @property
    def get_job(self) -> Callable[[jobs.GetJobRequest], jobs.Job]:
        r"""Return a callable for the get job method over gRPC.

        Gets the resource representation for a job in a
        project.

        Returns:
            Callable[[~.GetJobRequest],
                    ~.Job]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_job" not in self._stubs:
            self._stubs["get_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataproc.v1.JobController/GetJob",
                request_serializer=jobs.GetJobRequest.serialize,
                response_deserializer=jobs.Job.deserialize,
            )
        return self._stubs["get_job"]

    @property
    def list_jobs(self) -> Callable[[jobs.ListJobsRequest], jobs.ListJobsResponse]:
        r"""Return a callable for the list jobs method over gRPC.

        Lists regions/{region}/jobs in a project.

        Returns:
            Callable[[~.ListJobsRequest],
                    ~.ListJobsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_jobs" not in self._stubs:
            self._stubs["list_jobs"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataproc.v1.JobController/ListJobs",
                request_serializer=jobs.ListJobsRequest.serialize,
                response_deserializer=jobs.ListJobsResponse.deserialize,
            )
        return self._stubs["list_jobs"]

    @property
    def update_job(self) -> Callable[[jobs.UpdateJobRequest], jobs.Job]:
        r"""Return a callable for the update job method over gRPC.

        Updates a job in a project.

        Returns:
            Callable[[~.UpdateJobRequest],
                    ~.Job]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_job" not in self._stubs:
            self._stubs["update_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataproc.v1.JobController/UpdateJob",
                request_serializer=jobs.UpdateJobRequest.serialize,
                response_deserializer=jobs.Job.deserialize,
            )
        return self._stubs["update_job"]

    @property
    def cancel_job(self) -> Callable[[jobs.CancelJobRequest], jobs.Job]:
        r"""Return a callable for the cancel job method over gRPC.

        Starts a job cancellation request. To access the job resource
        after cancellation, call
        `regions/{region}/jobs.list <https://cloud.google.com/dataproc/docs/reference/rest/v1/projects.regions.jobs/list>`__
        or
        `regions/{region}/jobs.get <https://cloud.google.com/dataproc/docs/reference/rest/v1/projects.regions.jobs/get>`__.

        Returns:
            Callable[[~.CancelJobRequest],
                    ~.Job]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_job" not in self._stubs:
            self._stubs["cancel_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataproc.v1.JobController/CancelJob",
                request_serializer=jobs.CancelJobRequest.serialize,
                response_deserializer=jobs.Job.deserialize,
            )
        return self._stubs["cancel_job"]

    @property
    def delete_job(self) -> Callable[[jobs.DeleteJobRequest], empty.Empty]:
        r"""Return a callable for the delete job method over gRPC.

        Deletes the job from the project. If the job is active, the
        delete fails, and the response returns ``FAILED_PRECONDITION``.

        Returns:
            Callable[[~.DeleteJobRequest],
                    ~.Empty]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_job" not in self._stubs:
            self._stubs["delete_job"] = self.grpc_channel.unary_unary(
                "/google.cloud.dataproc.v1.JobController/DeleteJob",
                request_serializer=jobs.DeleteJobRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_job"]


__all__ = ("JobControllerGrpcTransport",)
