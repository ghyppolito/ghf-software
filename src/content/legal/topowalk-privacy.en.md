---
lastUpdated: "2026-10"
---
# Privacy Policy — TopoWalk

**Last updated:** October 2026

This Privacy Policy describes how the **TopoWalk** application, developed by **GHF Software**, handles user information. By using TopoWalk, you agree to the terms described in this document.

---

## 1. Who We Are

TopoWalk is an Android application developed by **GHF Software** for field topographic surveying purposes. We are not a data collection company.

Your surveys — points, measurements, photos, and reports — **remain on your device** and are not sent to any of our servers. The only exception is the **TopoWalk Pro migration service** described in section 2.11, which exists for a limited time, holds only an identifier with no name or email, and **does not touch your survey data**.

---

## 2. Data Accessed and Used by the Application

### 2.1 Location (GPS)

- **What is accessed:** Latitude, longitude, and altitude of points marked by the user during measurement.
- **Purpose:** Exclusively to perform topographic calculations (horizontal distance, elevation difference, slope distance, slope angle, azimuth, and polygon area) and to render the map visualization.
- **When it is accessed:** Only while the application is open and in active use (foreground). The app does not access location in the background.
- **Retention:** Location data is kept in memory during the session. If the user chooses to **save the measurement**, coordinates are stored locally in the device's database (see section 8.1). GHF Software does not send this data to its own servers; see section 8.4 regarding manual backup offered by TopoWalk and section 8.5 regarding automatic Android system backup, which may include this database in the user's own Google account.

### 2.2 Atmospheric Pressure Sensor (Barometer)

- **What is accessed:** Atmospheric pressure reading from the device's physical sensor.
- **Purpose:** To calculate the altitude of points with greater precision than GPS alone, using the standard barometric formula.
- **When it is accessed:** Continuously while the application is open, exclusively for converting pressure to altitude.
- **Retention:** Raw pressure values are not stored. Only the derived altitude is used for calculations and, optionally, saved with the measurement.

### 2.3 Bluetooth (External GNSS/RTK Receiver — optional, in Beta)

- **What is accessed:** Bluetooth connection with a previously paired external GNSS/RTK receiver chosen by the user, for reading position sentences (NMEA 0183).
- **Purpose:** To obtain high-precision coordinates and altitude from the external receiver instead of the device's internal GPS.
- **When it is accessed:** Only when the user explicitly enables the "External GNSS Receiver" feature and selects a device. The feature is **turned off by default**.
- **Scope:** The application **does not perform discovery** of devices and does not use the `BLUETOOTH_SCAN` permission; only devices already paired in Android settings are listed. Received data remains on the device, is used only for calculations and, optionally, saved with the measurement. **Nothing is transmitted to third parties.**
- **Beta Status:** The feature is flagged as Beta within the app. This does not alter the data handling described above — no additional information is collected due to the testing stage.

### 2.4 Internet Access (Map Tiles)

- **What is accessed:** The application makes HTTP requests to the **OpenStreetMap** (OpenTopoMap) tile network to display the relief map on the visualization screen.
- **Purpose:** To render the background relief map upon which the demarcation is plotted.
- **Data sent:** Only generic geographic coordinate data of necessary tiles for the visible area, without user identification.
- **When it is accessed:** Only when navigating to the "Map" tab within a measurement or in history.
- **Caching:** osmdroid may cache map tiles locally to improve performance. This cache contains only map images, no user personal data.

### 2.5 Point Names and Labels (from version 4.0)

- **What is accessed:** Optional text typed by the user to identify a captured point (e.g., "fence corner", "post 12").
- **Purpose:** Facilitate point recognition in the capture list, PDF report, and exported files.
- **Retention:** Stored along with the measurement, under the same terms as section 8.1. Never sent to GHF Software servers nor to Firebase.

### 2.6 Email Feedback (optional)

- **What happens:** On the external GNSS receiver screen, the "Send feedback" button opens the **user's own email application** with a pre-filled message addressed to `support@ghfsoftware.com`.
- **Pre-filled data in message:** TopoWalk version, Android version, and device manufacturer/model. No coordinates, measurement data, or history records are included.
- **User control:** The message is only sent if the user decides to send it, and they can edit or delete any part of the text beforehand. TopoWalk does not send anything automatically and does not have access to the user's email account.
- **What we receive:** By choosing to send, the user reveals to us the email address used, along with the message content. These emails are used exclusively to respond to and fix issues with the feature, are not shared with third parties or used for marketing, and can be deleted upon request to the same address.

### 2.7 Orientation Sensors — Compass (from version 4.1)

- **What is accessed:** Reading from the device's rotation vector sensor (which Android composes from magnetometer, accelerometer, and gyroscope), to determine where the device is pointing.
- **Purpose:** Exclusively to draw the arrow on the **Stakeout** screen, which guides the user to a previously surveyed point. Correction between magnetic north and geographic north is calculated on the device itself, from current position and Android's geomagnetic model.
- **When it is accessed:** Only while the Stakeout screen is open. The sensor is turned off upon exiting.
- **Retention:** Readings exist only in memory during screen use. **Nothing is stored or transmitted.** Devices without a compass simply do not display the arrow — the feature degrades to showing numeric azimuth.

### 2.8 Report Visual Identity (from version 4.1)

This is the only part of TopoWalk where users enter information **about themselves or their company**. Requires careful reading.

- **What the user can provide:** company name, technical manager name, professional registration (CREA, CAU, or equivalent), custom footer note, color accent, and an image file to serve as logo.
- **Purpose:** Compose header and footer of user-generated PDF reports, ensuring documents delivered to their clients reflect their company identity rather than the application's.
- **How logo is obtained:** via Android's native file picker (Storage Access Framework). The app **does not request storage permission** and **cannot view any other files** beyond the single file selected by the user. The image is resized and copied to the app's private area; the original file remains unchanged in its location.
- **Where this data resides:** exclusively on the device, in local app preferences and its private file area. **Never sent to GHF Software, Firebase, Google Play, or any third party.** Does not appear in analytics events or crash reports.
- **When this data leaves the device:** only when the **user explicitly shares** a PDF report — because it forms a visible part of the document, which is the feature's intended purpose. Sharing destination is chosen by the user and outside app control (same terms as section 8.2).
- **How to remove:** "Customize PDF Report" screen allows deleting logo and clearing fields at any time. Clearing app data also removes everything.

### 2.9 Imported Files — Reference Layers (from version 4.2)

- **What is accessed:** a single file at a time, chosen by the user in Android's native file picker (Storage Access Framework), in KML, KMZ, GeoJSON, GPX, or CSV formats. The application **does not ask for storage permissions** and **sees no other files** besides the user-selected file.
- **Purpose:** display boundary perimeters or points as reference map layers, and enable navigating to those points via Stakeout screen. Useful when users already have KML files from environmental/property registries or client files.
- **What the file may contain:** coordinates and point names designated by whoever created the file. This content may involve property data.
- **Where it stays:** content is copied to the **app's private directory on the device** (original file remains untouched in its original location). The copy exists because permission over selected file expires over time.
- **Where it does NOT go:** imported content is **never sent** to GHF Software, Firebase, Google Play, or any third party. It does not appear in analytics events or crash reports — only that an import occurred, format type, and point count are recorded, without any coordinates.
- **How to remove:** "Imported Layers" screen allows removing each layer at any time; removing deletes internal copy and does not touch original file. Clearing app data also removes everything.

### 2.10 Field Photos (from version 4.2)

This section describes the **only app data that may contain images of people or property**, and requires careful reading.

- **What the user can attach:** up to 5 photos per survey, taken via camera or chosen from device gallery.
- **Purpose:** document field conditions — survey mark, gate, erosion — alongside corresponding survey, and optionally include them in user-generated PDF report.
- **The app DOES NOT request camera or storage permissions.** Photos taken pass through system camera app (`ACTION_IMAGE_CAPTURE`), and gallery selection passes through Android photo picker — in both cases app only receives the selected file, **seeing no other photos on device**.
- **Where they stay:** app creates a **scaled-down copy** (max 1280 px, JPEG) in its private directory on device. Original photo remains unchanged. Copy exists because temporary URI provided by camera/gallery expires.
- **Metadata:** copy is saved **without original EXIF metadata** — including GPS tags recorded by camera. Only orientation is preserved and applied to image. In practice, copy saved by TopoWalk carries **less** info than original.
- **Where they do NOT go:** photos are **never sent** to GHF Software, Firebase, Google Play, or any third party. Not included in analytics or crash logs — only that photo was attached and photo count are recorded, without image or filename.
- **When they leave device:** only when **user shares** PDF report containing them — because they form a visible part of the document, which is the feature's purpose. Destination chosen by user (same terms as section 8.2).
- **How to remove:** photos can be individually deleted from survey screen. Deleting survey deletes photos. Clearing app data removes all. Original gallery photos are never touched.

### 2.11 TopoWalk Pro Migration to Google Account (from version 4.3)

Users who used TopoWalk before Pro existed received free access (section 6). This concession is stored **on device** and would not follow a phone switch automatically. This feature solves that: users request a **Google Play promo code**, redeem it on Play Store, and access becomes bound to their **Google account**.

This is the **only** feature of TopoWalk that stores anything on a server operated by GHF Software, and exists for a **limited time** — once migration ends, service is shut down and data below deleted.

**Deadline:** promo codes can be requested until **March 31, 2027**. After this date, service is permanently shut down and all records described in this section deleted.

- **When it happens:** only when user opens "Move Pro to your account" screen and taps request code. Users who never open this screen **establish no connection** with our server: app opens no session, generates no identifier, and sends nothing.
- **What is sent and stored:**
  - Hashed device identifier (SHA-256). Original ID is **not sent** and cannot be recovered from stored hash.
  - Anonymous session ID generated by Firebase — random number, no name, no email, no password. Not an account, requires no registration.
  - Date/time of request and promo code issued.
- **What is NOT sent:** name, email, Google account, payment data, location, surveys, photos, or any content created in app.
- **Purpose of hashed identifier:** promo codes are capped by Google per quarter. Without recognizing if a device was already served, repeated requests would exhaust inventory. Used **solely** to issue one code per device.
- **Integrity verification:** request includes **Google Play Integrity** attestation, confirming to our server that request originates from genuine TopoWalk app installed via Play Store. Done by Google, **reveals nothing about user**.
- **Storage location:** Cloud Firestore & Cloud Functions, hosted on Google Cloud under GHF Software account.
- **Retention period:** until **March 31, 2027** (deadline to request code). After campaign ends, records exported for audit and deleted, and service disabled.
- **How to request deletion:** write to `support@ghfsoftware.com` stating code received. We delete corresponding record.

---

## 3. Data NOT Collected

TopoWalk **does not collect, does not remotely store, and does not transmit**:

- Name, email, or any personally identifiable data — including in the Pro migration service (section 2.11), which **requires no login and receives no name or email**
- IP address or network data beyond what is needed to load map tiles and send analytics events and crash reports
- Background location or location history outside active app usage
- Advertising ID (the app explicitly removes this permission)

Three notes for precision:

1. **Email Feedback.** If user voluntarily writes to us via "Send feedback" button (section 2.6), we become aware of the email address chosen and content written. Always depends on explicit user action.
2. **TopoWalk Pro Migration (section 2.11).** This feature sends a hashed device ID and an anonymous session ID to our server. Neither carries name, email, or account, and neither is used outside this purpose. It is the **only** scenario where app stores anything on our server.
3. **Report Visual Identity (from version 4.1).** User can type their name and professional registration to appear on PDF (section 2.8). This data **is personal** but stays **solely on their device**: GHF Software does not receive, store, or access it. Leaves device only inside PDF user chooses to share.

---

## 4. Analytics — Firebase Analytics (Google)

Starting from version 3.10, TopoWalk uses **Firebase Analytics**, a usage analysis service provided by Google LLC.

### What is collected and sent to Firebase:

- **App interactions:** screens viewed, features used (e.g., capturing points, exporting files, accessing history), and navigation flow.
- **Interest in future formats (version 4.0):** export menu lists DXF and CSV as planned formats; tapping them records an anonymous event. **No contact collected in this flow** — app does not ask for email or phone. This measurement **ended in version 4.1** when both formats were introduced.
- **Purchase funnel (from version 4.1):** anonymous events recording purchase screen open, entry feature, purchase initiation, and completion/cancellation/failure. **Price, currency, payment method, Google account ID are NOT recorded** — only step in flow. Used to understand screen clarity, not to identify buyers.
- **Firebase installation ID:** anonymous identifier generated by SDK to aggregate sessions. Does not personally identify user and can be reset by uninstalling and reinstalling app.
- **Device information:** model, OS version, language — automatically collected by SDK.

### What is NOT collected by Firebase:

- GPS coordinates or topographic measurement data
- Name, email, or personal info entered in app
- Advertising ID (explicitly removed from app)

### Purpose:

Data is used exclusively to understand user interaction, identify most used features, and guide future improvements. Not used for advertising, personalization, or profiling.

### Retention and control:

Data is retained by Google in accordance with the [Google Privacy Policy](https://policies.google.com/privacy). User can clear Firebase installation ID by uninstalling app.

---

## 5. Error Reports — Firebase Crashlytics (Google)

Starting from version 3.13, TopoWalk uses **Firebase Crashlytics**, a Google LLC service for crash reporting. Detects issues users cannot report on their own — especially external GNSS/RTK receiver connection failures occurring in field without useful error messages.

### What is collected and sent to Crashlytics:

- **Application crashes:** exception type, stack trace, and thread state at time of error.
- **Non-fatal external receiver failures:** disconnection reason, original Bluetooth exception, attempt count, and a snippet of up to 16 characters from start of receiver data stream — deliberately short to contain only sentence header (type and time), never coordinates.
- **Session technical context:** whether external receiver is enabled, paired model name, connection state, fix quality (e.g. `RTK_FIXED`), satellite count, and HDOP.
- **Purchase and logo reading failures (from version 4.1):** error code returned by Google Play when purchase confirmation is not accepted, and stack trace of an unreadable logo image. **Neither contains image content, company data, price, or account ID.**
- **Device information and Firebase installation ID:** automatically collected by SDK under same terms as section 4.

### What is NOT collected by Crashlytics:

- GPS coordinates, altitudes, or survey data
- Survey names, notes, or exported files
- Name, email, or personal info entered in app
- Logo, company name, technical manager, or professional registration (section 2.8)

### Purpose:

Exclusively to diagnose and fix application defects. Data is not used for advertising, personalization, or profiling.

### Retention and control:

Reports are retained by Google in accordance with the [Google Privacy Policy](https://policies.google.com/privacy) and [Crashlytics documentation](https://firebase.google.com/support/privacy).

---

## 6. In-App Purchases — Google Play Billing (from version 4.1)

Starting from version 4.1, TopoWalk offers a **one-time lifetime purchase** (TopoWalk Pro), processed by **Google Play Billing**, a Google LLC service.

### Who processes payment

**Payment is processed entirely by Google.** TopoWalk **never** sees, receives, or stores credit card numbers, bank details, billing addresses, or payment information. This screen belongs to Google Play, not the app, governed by [Google Privacy Policy](https://policies.google.com/privacy) and Google Play Terms of Service.

### What the app sends to Google Play

- Product ID (`topowalk_pro`) to query price and open purchase screen.
- Acknowledgment that purchase was received (required by Google; without it, purchase is automatically refunded in three days).

The app **sends no developer-created account, user, or device ID** to Google Play. Developer obfuscated account ID features (`obfuscatedAccountId`) **are not used**.

TopoWalk **has no user accounts**: no registration, login, password, or profile. Pro migration service (section 2.11) uses an anonymous Firebase session — random ID generated by device, not an account, asking for no credentials and storing no name or email.

### What the app receives and stores

- **Formatted price** in user's currency to display on screen. App does not know currency or country — receives ready text from Google.
- **Whether an active purchase exists** for device, queried on app launch. Stored locally as boolean "yes/no" so app does not flicker "unpurchased" during query. **No Google account data is stored.**

### Why query repeats

Verification happens every session because that is how a **refund** reaches the app: if user requests refund from Google, purchase status updates and access is revoked. Conversely, reinstalling app restores access without repurchasing.

### Access granted without purchase

Users who had TopoWalk installed before TopoWalk Pro launch receive access **for free and permanently**. Concession recorded **on device only**, involving no Google Play, user account, or personal data.

Being recorded on device, it would not follow a phone switch automatically. To solve this, section 2.11 offers **Pro migration**: user requests a promo code, redeems on Play Store, and access becomes bound to their Google account — returning on any device logged into the same account.

### Minors

Google Play purchases are subject to Google Play parental controls and authentication requirements. TopoWalk does not perform age verification.

---

## 7. Data Sharing with Third Parties

TopoWalk shares data with the following third parties:

| Third Party | Shared Data | Purpose |
|---|---|---|
| **Google LLC (Firebase Analytics)** | App interactions, installation ID, device info | Usage analytics |
| **Google LLC (Firebase Crashlytics)** | Stack traces, external receiver failures, session technical context, installation ID, device info | Failure diagnostics |
| **OpenStreetMap / OpenTopoMap** | Coordinates of requested map tiles | Map rendering |
| **Google LLC (Google Play Billing)** — from version 4.1 | Product ID and purchase acknowledgment. No developer account ID; no payment data passes through app | Process TopoWalk Pro purchase |
| **Google LLC (Firebase Authentication)** — Pro migration, section 2.11 | An **anonymous** session: random identifier generated by device. No name, no email, no password | Identify call to migration service |
| **GHF Software (Cloud Firestore & Cloud Functions on Google Cloud)** — Pro migration, section 2.11 | Hashed device ID, anonymous session ID, date/time of request, issued promo code | Deliver one code per device and prevent inventory exhaustion |

The application does not integrate SDKs for advertising, social networks, or any other external service beyond those listed above.

---

## 8. Local Storage

### 8.1 Database (Measurement History)

When the user chooses to save a measurement, the following data is stored **locally on the device** in a Room (SQLite) database, accessible only by the application:

- Name and notes entered by the user
- Coordinates (latitude, longitude, altitude) of each measurement point
- Calculated results (distances, elevation differences, angles, area)
- Date and time of measurement

This data is **never sent to GHF Software servers** and remains on the device until manually deleted by the user through the app or by clearing app data. See section 8.4 regarding manual backup offered by TopoWalk, and section 8.5 regarding automatic Android system backup — the two are independent of each other.

### 8.2 PDF Reports

When requesting PDF report generation, the application:

1. Creates the PDF file temporarily in the app's **private cache directory** (`cacheDir`), accessible only by the app itself.
2. Shares the file via `FileProvider` with the app of your choice (WhatsApp, email, Google Drive, etc.) using Android's standard mechanism.
3. The file remains in the cache until it is deleted: the app removes export files older than 24 hours on each new DXF, CSV, GeoJSON, KML, or GPX export, and the operating system may also clear the cache automatically. The user can also clear the app data.

TopoWalk has no access to the destination chosen by the user for sharing — this operation is managed entirely by the Android system and the receiving application.

### 8.3 Exporting Files

Users can export measurements in **GeoJSON, KML, and GPX** (from version 4.0) and in **DXF and CSV** (from version 4.1). These files are generated locally in the device's cache and shared in the same way as the PDF (section 8.2), including how long they remain in the cache: files older than 24 hours are deleted by the app on the next export. The app has no access to the sharing destination.

CSV export generates **two files** — one with points and another with segments —, shared together. DXF contains, in addition to geometry, the latitude and longitude of the first survey point, recorded as text inside the file to allow positioning the drawing; it is the same coordinate data carried by other formats.

### 8.4 History Backup and Restore (from version 4.0)

TopoWalk allows users to manually export **all measurement history** into a single file and restore it later — on the same device after reinstallation, or on another device.

- **How it works:** when tapping "Backup history", the app uses Android's own file picker (Storage Access Framework) so the user can choose where to save the file — Google Drive, SD card, internal storage, or any other location listed by the system. **The app writes directly to the location chosen by the user**, without using the inter-app share picker used for PDF and other formats (sections 8.2 and 8.3), and without sending the file to GHF Software servers.
- **What the file contains:** name, notes, coordinates, altitude, calculated results, and point labels for each saved measurement — the same data described in section 8.1 gathered into a single file.
- **Restore:** upon choosing "Restore backup" and selecting a file (via the same system picker), measurements from the file are added to the device history. Nothing already saved is erased, and existing measurements are identified and not duplicated. A file generated by a newer TopoWalk version than the installed one will be rejected to prevent local database corruption.
- **User control:** GHF Software has no access to this file at any time — it exists solely in the location chosen by the user, under their control and responsibility (including the security of their own Google Drive account if that is the chosen destination).

This mechanism is independent of the automatic Android System Backup described in section 8.5.

### 8.5 Automatic Android System Backup

TopoWalk **does not operate any proprietary cloud backup or sync service**. However, the application does not disable Android's **Automatic Backup** feature ("Backup by Google"), which is an operating system mechanism independent of TopoWalk:

- If the user has this feature enabled on their Google account (default on most Android devices) and the device meets conditions set by Android (connected to Wi-Fi, charging, and idle), the OS may periodically in the background include TopoWalk data — including the local measurement history database — in the user's Google account backup.
- This backup is stored and managed by **Google infrastructure** associated with the user's own Google account — GHF Software has no access to this backup, does not receive it, control it, or delete it.
- Should the user reinstall TopoWalk on the same or another device connected to the same Google account, Android may automatically restore this data from that backup.
- Users who do not wish measurement history to be included in this system backup can disable "Google Backup" for the device, or specifically for TopoWalk, in Android settings (Settings → System → Backup, varying by manufacturer and Android version).

**Note regarding report visual identity (section 2.8):** the copied logo and company data reside in private app storage and preferences, and therefore may also be included in this automatic system backup — in the user's own Google account, always out of reach of GHF Software. Anyone wishing to avoid this can disable system backup as described above.

This section describes standard Android behavior for data management. It does not alter any other commitment in this policy: GHF Software continues not to operate user data storage servers and never has access to this content.

### 8.6 Data Outside the Device (Pro Migration)

All of section 8 describes storage **on the device itself**. The sole exception in the application is the Pro migration service (section 2.11), which stores a hashed device ID, an anonymous session ID, request date, and issued code on a GHF Software server — nothing more, and nothing identifying a person. Surveys, photos, and reports **never** leave the device through this path.

---

## 9. Application Permissions

| Permission | Reason |
|---|---|
| `ACCESS_FINE_LOCATION` | Obtain precise GPS coordinates for measurement points |
| `ACCESS_COARSE_LOCATION` | Complementary permission required by Android for location |
| `INTERNET` | Load OpenStreetMap map tiles, send events to Firebase Analytics and crash reports to Crashlytics, and, **when the user requests Pro migration** (section 2.11), communicate with our server |
| `VIBRATE` | Haptic feedback when capturing a measurement point |
| `BLUETOOTH_CONNECT` (Android 12+) | Connect to a previously paired external GNSS/RTK receiver when the feature is enabled by the user |
| `BLUETOOTH` / `BLUETOOTH_ADMIN` (Android 11 and earlier) | Equivalent for older Android versions for the same connection |
| `com.android.vending.BILLING` (from version 4.1) | Required by Google Play to offer TopoWalk Pro purchase. Added automatically by Google library and **grants no access to device data** |

**The compass used in Stakeout (section 2.7) and logo selection (section 2.8) require no permissions:** orientation sensors are free in Android, and the file picker delivers only the single file selected by the user.

The application does not request access to microphone, contacts, or external storage. **Nor does it request camera permission** — field photos (section 2.10) enter via system camera app and Android photo picker, which deliver to TopoWalk only the user-selected file. Advertising ID (`AD_ID`) is explicitly removed from app and not collected.

---

## 10. Use by Minors

TopoWalk is not directed to children under 13 and does not intentionally collect data from minors. Being a technical field tool, use by minors should occur under supervision of a responsible adult.

Starting from version 4.1, TopoWalk Pro purchase is processed by Google Play and is subject to Google Play parental controls and authentication requirements (section 6). TopoWalk does not perform age verification of its own.

---

## 11. Security

TopoWalk measurement data is processed and stored exclusively on the user's device. Communication with external services (Firebase Analytics and OpenStreetMap) is performed exclusively via HTTPS with encryption in transit. Data sent to Firebase does not contain personally identifiable information. The security of locally stored data is managed by the Android operating system and app sandboxing.

Starting from version 4.1, **no payment data passes through the application**: purchase is conducted entirely via Google Play screen, and TopoWalk receives back only information on whether an active purchase exists (section 6).

---

## 12. Changes to this Policy

We may update this Privacy Policy periodically. Relevant changes will be communicated via a new version of the application published on the Google Play Store. The "Last updated" date at the top of this document will always reflect the current version.

We recommend that you review this policy periodically.

---

## 13. Contact

Questions, requests, or comments about this Privacy Policy can be sent to:

**GHF Software**\
Email: **support@ghfsoftware.com**

---

*This policy was prepared in compliance with the General Data Protection Law (LGPD — Law No. 13,709/2018), the European Union General Data Protection Regulation (GDPR), and Google Play Store privacy policies.*
