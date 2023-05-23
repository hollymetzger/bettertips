import os
from square.client import Client

client = Client(
    access_token=os.environ['SQUARE_ACCESS_TOKEN'],
    environment='production')

def get_active_shifts(location_id, time):
        wages = client.team
        print(type(client.team))
get_active_shifts('locationid', '2023-05-12T15:37:00.828Z')
    

def gret_active_shifts(api_instance, location_id, time):
    try:
        # List employee wages for all employees at the specified location
        wages = api_instance.list_employee_wages(location_ids=[location_id]).employee_wages
        
        # Filter employee wages to only include those with active shifts during the specified time
        active_employee_ids = []
        for wage in wages:
            if wage.employee_id not in active_employee_ids:
                try:
                    # List shifts for this employee during the specified time
                    shifts = api_instance.list_shifts(employee_id=wage.employee_id, location_ids=[location_id], start_time=time, end_time=time).shifts
                    
                    # Check if the employee had an active shift during the specified time
                    for shift in shifts:
                        if shift.is_open:
                            active_employee_ids.append(wage.employee_id)
                            break
                except ApiException as e:
                    print("Exception when calling ShiftsApi->list_shifts: %s\n" % e)
        
        # List all shifts for the specified location during the specified time
        shifts = api_instance.list_shifts(location_ids=[location_id], start_time=time, end_time=time).shifts
        
        # Filter shifts to only include those for active employees
        active_shifts = []
        for shift in shifts:
            if shift.employee_id in active_employee_ids:
                active_shifts.append(shift)
        
        return active_shifts
    
    except ApiException as e:
        print("Exception when calling API: %s\n" % e)



def getemployeeids():
    members = []
    
    # Call the Square API to retrieve team members
    response = client.team.search_team_members(
        body = {
            "query": {
                "filter": {
                    "location_ids": [
                        "LTJZEPEWD0KK8"
                    ],
                    "status": "ACTIVE"
                }
            },
        }
    )

    # Extract the member data from the API response
    if response.is_success():
        for member in response.body['team_members']:
            members.append({'id': member['id'], 'name': member['given_name']})
    else:
        print(response.errors)

    return members


def getAShift():
  actives = []

  result = client.labor.search_shifts(
    body = {
      "query": {
        "filter": {
          "workday": {
            "date_range": {
              "start_date": "2023-03-01",
              "end_date": "2023-03-02"
            },
            "match_shifts_by": "START_AT",
            "default_timezone": "America/New_York"
          }
        }
      },
      "limit": 1
    }
  )

  if result.is_success():
    actives.append(result.body)
  elif result.is_error():
    print(result.errors)

  return actives



actives = getAShift()

#for shift in actives:
  # print(shift)



def getAllActives():
  result = client.team.search_team_members(
  body = {
    "query": {
      "filter": {
        "location_ids": [
          "LTJZEPEWD0KK8"
        ],
        "status": "ACTIVE"
      }
    },
    "limit": 3
  }
  )

  if result.is_success():
    print(result.body)
  elif result.is_error():
    print(result.errors)


# -*- coding: utf-8 -*-

from square.api_helper import APIHelper
from square.http.api_response import ApiResponse
from square.api.base_api import BaseApi
from apimatic_core.request_builder import RequestBuilder
from apimatic_core.response_handler import ResponseHandler
from apimatic_core.types.parameter import Parameter
from square.http.http_method_enum import HttpMethodEnum
from apimatic_core.authentication.multiple.single_auth import Single
from apimatic_core.authentication.multiple.and_auth_group import And
from apimatic_core.authentication.multiple.or_auth_group import Or


class TeamApi(BaseApi):

    """A Controller to access Endpoints in the square API."""
    def __init__(self, config):
        super(TeamApi, self).__init__(config)

    def create_team_member(self,
                           body):
        """Does a POST request to /v2/team-members.

        Creates a single `TeamMember` object. The `TeamMember` object is
        returned on successful creates.
        You must provide the following values in your request to this
        endpoint:
        - `given_name`
        - `family_name`
        Learn about [Troubleshooting the Team
        API](https://developer.squareup.com/docs/team/troubleshooting#createtea
        mmember).

        Args:
            body (CreateTeamMemberRequest): An object containing the fields to
                POST for the request.  See the corresponding object definition
                for field details.

        Returns:
            ApiResponse: An object with the response value as well as other
                useful information such as status codes and headers. Success

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        return super().new_api_call_builder.request(
            RequestBuilder().server('default')
            .path('/v2/team-members')
            .http_method(HttpMethodEnum.POST)
            .header_param(Parameter()
                          .key('Content-Type')
                          .value('application/json'))
            .body_param(Parameter()
                        .value(body))
            .header_param(Parameter()
                          .key('accept')
                          .value('application/json'))
            .body_serializer(APIHelper.json_serialize)
            .auth(Single('global'))
        ).response(
            ResponseHandler()
            .deserializer(APIHelper.json_deserialize)
            .is_api_response(True)
            .convertor(ApiResponse.create)
        ).execute()

    def bulk_create_team_members(self,
                                 body):
        """Does a POST request to /v2/team-members/bulk-create.

        Creates multiple `TeamMember` objects. The created `TeamMember`
        objects are returned on successful creates.
        This process is non-transactional and processes as much of the request
        as possible. If one of the creates in
        the request cannot be successfully processed, the request is not
        marked as failed, but the body of the response
        contains explicit error information for the failed create.
        Learn about [Troubleshooting the Team
        API](https://developer.squareup.com/docs/team/troubleshooting#bulk-crea
        te-team-members).

        Args:
            body (BulkCreateTeamMembersRequest): An object containing the
                fields to POST for the request.  See the corresponding object
                definition for field details.

        Returns:
            ApiResponse: An object with the response value as well as other
                useful information such as status codes and headers. Success

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        return super().new_api_call_builder.request(
            RequestBuilder().server('default')
            .path('/v2/team-members/bulk-create')
            .http_method(HttpMethodEnum.POST)
            .header_param(Parameter()
                          .key('Content-Type')
                          .value('application/json'))
            .body_param(Parameter()
                        .value(body))
            .header_param(Parameter()
                          .key('accept')
                          .value('application/json'))
            .body_serializer(APIHelper.json_serialize)
            .auth(Single('global'))
        ).response(
            ResponseHandler()
            .deserializer(APIHelper.json_deserialize)
            .is_api_response(True)
            .convertor(ApiResponse.create)
        ).execute()

    def bulk_update_team_members(self,
                                 body):
        """Does a POST request to /v2/team-members/bulk-update.

        Updates multiple `TeamMember` objects. The updated `TeamMember`
        objects are returned on successful updates.
        This process is non-transactional and processes as much of the request
        as possible. If one of the updates in
        the request cannot be successfully processed, the request is not
        marked as failed, but the body of the response
        contains explicit error information for the failed update.
        Learn about [Troubleshooting the Team
        API](https://developer.squareup.com/docs/team/troubleshooting#bulk-upda
        te-team-members).

        Args:
            body (BulkUpdateTeamMembersRequest): An object containing the
                fields to POST for the request.  See the corresponding object
                definition for field details.

        Returns:
            ApiResponse: An object with the response value as well as other
                useful information such as status codes and headers. Success

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        return super().new_api_call_builder.request(
            RequestBuilder().server('default')
            .path('/v2/team-members/bulk-update')
            .http_method(HttpMethodEnum.POST)
            .header_param(Parameter()
                          .key('Content-Type')
                          .value('application/json'))
            .body_param(Parameter()
                        .value(body))
            .header_param(Parameter()
                          .key('accept')
                          .value('application/json'))
            .body_serializer(APIHelper.json_serialize)
            .auth(Single('global'))
        ).response(
            ResponseHandler()
            .deserializer(APIHelper.json_deserialize)
            .is_api_response(True)
            .convertor(ApiResponse.create)
        ).execute()

    def search_team_members(self,
                            body):
        """Does a POST request to /v2/team-members/search.

        Returns a paginated list of `TeamMember` objects for a business.
        The list can be filtered by the following:
        - location IDs
        - `status`

        Args:
            body (SearchTeamMembersRequest): An object containing the fields
                to POST for the request.  See the corresponding object
                definition for field details.

        Returns:
            ApiResponse: An object with the response value as well as other
                useful information such as status codes and headers. Success

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        return super().new_api_call_builder.request(
            RequestBuilder().server('default')
            .path('/v2/team-members/search')
            .http_method(HttpMethodEnum.POST)
            .header_param(Parameter()
                          .key('Content-Type')
                          .value('application/json'))
            .body_param(Parameter()
                        .value(body))
            .header_param(Parameter()
                          .key('accept')
                          .value('application/json'))
            .body_serializer(APIHelper.json_serialize)
            .auth(Single('global'))
        ).response(
            ResponseHandler()
            .deserializer(APIHelper.json_deserialize)
            .is_api_response(True)
            .convertor(ApiResponse.create)
        ).execute()

    def retrieve_team_member(self,
                             team_member_id):
        """Does a GET request to /v2/team-members/{team_member_id}.

        Retrieves a `TeamMember` object for the given `TeamMember.id`.
        Learn about [Troubleshooting the Team
        API](https://developer.squareup.com/docs/team/troubleshooting#retrieve-
        a-team-member).

        Args:
            team_member_id (string): The ID of the team member to retrieve.

        Returns:
            ApiResponse: An object with the response value as well as other
                useful information such as status codes and headers. Success

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        return super().new_api_call_builder.request(
            RequestBuilder().server('default')
            .path('/v2/team-members/{team_member_id}')
            .http_method(HttpMethodEnum.GET)
            .template_param(Parameter()
                            .key('team_member_id')
                            .value(team_member_id)
                            .should_encode(True))
            .header_param(Parameter()
                          .key('accept')
                          .value('application/json'))
            .auth(Single('global'))
        ).response(
            ResponseHandler()
            .deserializer(APIHelper.json_deserialize)
            .is_api_response(True)
            .convertor(ApiResponse.create)
        ).execute()

    def update_team_member(self,
                           team_member_id,
                           body):
        """Does a PUT request to /v2/team-members/{team_member_id}.

        Updates a single `TeamMember` object. The `TeamMember` object is
        returned on successful updates.
        Learn about [Troubleshooting the Team
        API](https://developer.squareup.com/docs/team/troubleshooting#update-a-
        team-member).

        Args:
            team_member_id (string): The ID of the team member to update.
            body (UpdateTeamMemberRequest): An object containing the fields to
                POST for the request.  See the corresponding object definition
                for field details.

        Returns:
            ApiResponse: An object with the response value as well as other
                useful information such as status codes and headers. Success

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        return super().new_api_call_builder.request(
            RequestBuilder().server('default')
            .path('/v2/team-members/{team_member_id}')
            .http_method(HttpMethodEnum.PUT)
            .template_param(Parameter()
                            .key('team_member_id')
                            .value(team_member_id)
                            .should_encode(True))
            .header_param(Parameter()
                          .key('Content-Type')
                          .value('application/json'))
            .body_param(Parameter()
                        .value(body))
            .header_param(Parameter()
                          .key('accept')
                          .value('application/json'))
            .body_serializer(APIHelper.json_serialize)
            .auth(Single('global'))
        ).response(
            ResponseHandler()
            .deserializer(APIHelper.json_deserialize)
            .is_api_response(True)
            .convertor(ApiResponse.create)
        ).execute()

    def retrieve_wage_setting(self,
                              team_member_id):
        """Does a GET request to /v2/team-members/{team_member_id}/wage-setting.

        Retrieves a `WageSetting` object for a team member specified
        by `TeamMember.id`.
        Learn about [Troubleshooting the Team
        API](https://developer.squareup.com/docs/team/troubleshooting#retrievew
        agesetting).

        Args:
            team_member_id (string): The ID of the team member for which to
                retrieve the wage setting.

        Returns:
            ApiResponse: An object with the response value as well as other
                useful information such as status codes and headers. Success

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        return super().new_api_call_builder.request(
            RequestBuilder().server('default')
            .path('/v2/team-members/{team_member_id}/wage-setting')
            .http_method(HttpMethodEnum.GET)
            .template_param(Parameter()
                            .key('team_member_id')
                            .value(team_member_id)
                            .should_encode(True))
            .header_param(Parameter()
                          .key('accept')
                          .value('application/json'))
            .auth(Single('global'))
        ).response(
            ResponseHandler()
            .deserializer(APIHelper.json_deserialize)
            .is_api_response(True)
            .convertor(ApiResponse.create)
        ).execute()

    def update_wage_setting(self,
                            team_member_id,
                            body):
        """Does a PUT request to /v2/team-members/{team_member_id}/wage-setting.

        Creates or updates a `WageSetting` object. The object is created if a
        `WageSetting` with the specified `team_member_id` does not exist.
        Otherwise,
        it fully replaces the `WageSetting` object for the team member.
        The `WageSetting` is returned on a successful update.
        Learn about [Troubleshooting the Team
        API](https://developer.squareup.com/docs/team/troubleshooting#create-or
        -update-a-wage-setting).

        Args:
            team_member_id (string): The ID of the team member for which to
                update the `WageSetting` object.
            body (UpdateWageSettingRequest): An object containing the fields
                to POST for the request.  See the corresponding object
                definition for field details.

        Returns:
            ApiResponse: An object with the response value as well as other
                useful information such as status codes and headers. Success

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """

        return super().new_api_call_builder.request(
            RequestBuilder().server('default')
            .path('/v2/team-members/{team_member_id}/wage-setting')
            .http_method(HttpMethodEnum.PUT)
            .template_param(Parameter()
                            .key('team_member_id')
                            .value(team_member_id)
                            .should_encode(True))
            .header_param(Parameter()
                          .key('Content-Type')
                          .value('application/json'))
            .body_param(Parameter()
                        .value(body))
            .header_param(Parameter()
                          .key('accept')
                          .value('application/json'))
            .body_serializer(APIHelper.json_serialize)
            .auth(Single('global'))
        ).response(
            ResponseHandler()
            .deserializer(APIHelper.json_deserialize)
            .is_api_response(True)
            .convertor(ApiResponse.create)
        ).execute()