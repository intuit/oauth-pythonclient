 # Copyright (c) 2018 Intuit
 #
 # Licensed under the Apache License, Version 2.0 (the "License");
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 #
 #  http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.
 
"""This module contains Enum values used by this library
"""

from enum import Enum

class Scopes(Enum):
    """Scopes supported by Intuit for OAuth and OpenID flows
    """

    PROFILE = 'profile'
    EMAIL = 'email'
    PHONE = 'phone'
    ADDRESS = 'address'
    OPENID = 'openid'
    ACCOUNTING = 'com.intuit.quickbooks.accounting'
    PAYMENT = 'com.intuit.quickbooks.payment'
    
    # for whitelisted Beta apps only
    PAYROLL = 'com.intuit.quickbooks.payroll'
    PAYROLL_TIMETRACKING = 'com.intuit.quickbooks.payroll.timetracking'
    PAYROLL_BENEFITS = 'com.intuit.quickbooks.payroll.benefits'
    PAYSLIP_READ = 'com.intuit.quickbooks.payroll.payslip.read'

    # For migrated apps only
    # To not see consent page they should pass the following scopes - openid intuit_name email
    INTUIT_NAME = 'intuit_name'