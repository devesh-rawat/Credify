import 'package:flutter/material.dart';

class AppColors {
  // DARK MODE COLORS
  static const Color darkBackground = Color(0xFF0A1A33);
  static const Color darkCard = Color(0xFF0D243A);
  static const Color darkInput = Color(0xFF0F2A45);

  static const Color darkPrimaryBlue = Color(0xFF1A73E8);
  static const Color darkAccentBlue = Color(0xFF3EA6FF);
  static const Color darkCyan = Color(0xFF4CC9F0);

  static const Color darkText = Color(0xFFFFFFFF);
  static const Color darkTextSecondary = Color(0xFFD9E2EC);
  static const Color darkMuted = Color(0xFF8EA3B7);

  // LIGHT MODE COLORS
  static const Color lightBackground = Color(0xFFFFFFFF);
  static const Color lightCard = Color(0xFFF6F7F9);

  static const Color lightPrimaryBlue = Color(0xFF1A73E8);
  static const Color lightInput = Color(0xFFF0F3F8);

  static const Color lightText = Color(0xFF1C1C1C);
  static const Color lightTextSecondary = Color(0xFF6E7C87);
}

ThemeData lightTheme = ThemeData(
  brightness: Brightness.light,
  scaffoldBackgroundColor: AppColors.lightBackground,
  primaryColor: AppColors.lightPrimaryBlue,
  fontFamily: 'Poppins',

  appBarTheme: AppBarTheme(
    backgroundColor: AppColors.lightBackground,
    foregroundColor: AppColors.lightText,
    elevation: 0,
  ),

  cardColor: AppColors.lightCard,

  textTheme: TextTheme(
    bodyLarge: TextStyle(color: AppColors.lightText),
    bodyMedium: TextStyle(color: AppColors.lightTextSecondary),
  ),

  inputDecorationTheme: InputDecorationTheme(
    filled: true,
    fillColor: AppColors.lightInput,
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: BorderSide.none,
    ),
  ),

  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      backgroundColor: AppColors.lightPrimaryBlue,
      foregroundColor: Colors.white,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      minimumSize: const Size(double.infinity, 55),
    ),
  ),
);


ThemeData darkTheme = ThemeData(
  brightness: Brightness.dark,
  scaffoldBackgroundColor: AppColors.darkBackground,
  primaryColor: AppColors.darkPrimaryBlue,
  fontFamily: 'Poppins',

  appBarTheme: AppBarTheme(
    backgroundColor: AppColors.darkBackground,
    foregroundColor: AppColors.darkText,
    elevation: 0,
  ),

  cardColor: AppColors.darkCard,

  textTheme: TextTheme(
    bodyLarge: TextStyle(color: AppColors.darkText),
    bodyMedium: TextStyle(color: AppColors.darkTextSecondary),
  ),

  inputDecorationTheme: InputDecorationTheme(
    filled: true,
    fillColor: AppColors.darkInput,
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(12),
      borderSide: BorderSide.none,
    ),
  ),

  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      backgroundColor: AppColors.darkPrimaryBlue,
      foregroundColor: Colors.white,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      minimumSize: const Size(double.infinity, 55),
    ),
  ),
);



