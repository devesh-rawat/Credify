
import 'package:credifyapp/screens/applications/application_screen.dart';
import 'package:credifyapp/screens/applications/apply_loan_screen.dart';
import 'package:credifyapp/screens/auth/auth_screen.dart';
import 'package:credifyapp/screens/chatbot/chat_screen.dart';
import 'package:credifyapp/screens/consent/consent_screen.dart';
import 'package:credifyapp/screens/dashboard/dashboard_screen.dart';
import 'package:credifyapp/screens/emicalculator/emi_calculator_screen.dart';
import 'package:credifyapp/screens/guidelines/guidelines_screen.dart';
import 'package:credifyapp/screens/profile/profile_screen.dart';
import 'package:credifyapp/screens/score/score_screen.dart';
import 'package:credifyapp/screens/showbanks/showlinked_bank.dart';
import 'package:credifyapp/screens/splash/splash_screen.dart';
import 'package:credifyapp/screens/verifyaccountscreen/verify_account_screen.dart';
import 'package:credifyapp/screens/verifyotp/verify_otp_screen.dart';
import 'package:flutter/material.dart';


class AppRoutes {
  static const splash = "/";
  static const login = "/login";
  static const consent = "/consent";
  static const showBankScreen = "/showBankScreen";
  static const showLinkedBank="/showLinkedBank";
  static const verifyAccount="/verifyAccount";
  static const verifyOTP = "/verifyOTP";
  static const chatbot = "/chatbot";
  static const applications="/applications";
  static const guidelines="/guidelines";
  static const dashboard = "/dashboard";
  static const score = "/report";
  static const calculator = "/calculator";
  static const profile = "/profile";
  static const questions="/questions";
  static const applyLoan = "/applyLoan";

  static Map<String, WidgetBuilder> routes = {
    splash: (_) => const SplashScreen(),
    login:(_)=>const AuthScreen(),
    consent:(_)=>const ConsentScreen(),
    verifyAccount:(_)=>VerifyAccountScreen(),
    verifyOTP:(_)=>VerifyOtpScreen(),
    score:(_)=>const ScoreScreen(),
    dashboard:(_)=>DashboardScreen(),
    guidelines:(_)=>const RBIGuidelinesScreen(),
    chatbot:(_)=>ChatScreen(),
    profile:(_)=>ProfileScreen(),
    showLinkedBank:(_)=>ShowLinkedBank(),
    calculator:(_)=>EmiCalculatorScreen(),
    applications:(_)=>LoanApplicationsScreen(),
    applyLoan:(_)=>const ApplyLoanScreen(),
   
    
  };
}
