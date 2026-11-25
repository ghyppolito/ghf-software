---
lastUpdated: "2026-11"
origemCommit: "cfbff63d47b59e5c97f4c6dce74ac88cef216070"
---
# Privacy Policy — TopoWalk

**Last updated:** November 2026

This Privacy Policy describes how the **TopoWalk** app, developed by **GHF Software**, handles user information: what is used, for what purpose, on what legal basis, for how long, and what your rights are. The rules for using the app are set out in the [Terms of Use](TERMS_OF_USE.en.md).

---

## 1. Who We Are

TopoWalk is an Android app developed by **GHF Software** for field topographic surveying. We are not a data collection company.

**Data controller** (Art. 5(VI) LGPD — Brazilian General Data Protection Law, Law No. 13,709/2018; Art. 4(7) GDPR): **GHF Software**, the trade name of ‹fill in: full name›, an individual, ‹fill in: city/state›, Brazil — email **support@ghfsoftware.com**. No separate data protection officer (DPO) has been appointed; this same email address handles all requests concerning personal data (section 13).

Your surveys — points, measurements, photos and reports — **stay on your device** and are not sent to any server of ours. The only exception is the **TopoWalk Pro migration** service described in section 2.11, which exists for a limited time, stores only an identifier with no name or email, and **does not touch your survey data**.

---

## 2. Data Accessed and Used by the App

### 2.1 Location (GPS)

- **What is accessed:** Latitude, longitude and altitude of the points marked by the user during measurement.
- **Purpose:** Exclusively to perform the topographic calculations (horizontal distance, height difference, slope distance, slope angle, azimuth and polygon area) and to generate the map view.
- **When it is accessed:** Only while the app is open and in active use (foreground). The app does not access location in the background.
- **Retention:** Location data is kept in memory during the session. If the user chooses to **save the measurement**, the coordinates are stored locally in the device's database (see section 8.1). GHF Software does not send this data to its own servers; see section 8.4 on the manual backup that TopoWalk itself offers and section 8.5 on Android's system automatic backup, which may include this database in the user's own Google account.

### 2.2 Atmospheric Pressure Sensor (Barometer)

- **What is accessed:** Atmospheric pressure readings from the device's physical sensor.
- **Purpose:** To calculate the altitude of points more accurately than GPS alone, using the standard barometric formula.
- **When it is accessed:** Continuously while the app is open, exclusively to convert pressure into altitude.
- **Retention:** Raw pressure values are not stored. Only the derived altitude is used in calculations and, optionally, saved with the measurement.

### 2.3 Bluetooth (External GNSS/RTK Receiver — optional, in Beta)

- **What is accessed:** A Bluetooth connection to an already-paired external GNSS/RTK receiver chosen by the user, to read position sentences (NMEA 0183).
- **Purpose:** To obtain high-accuracy coordinates and altitude from the external receiver instead of the device's internal GPS.
- **When it is accessed:** Only when the user explicitly turns on the "External GNSS receiver" feature and selects a device. The feature is **off by default**.
- **Scope:** The app **does not perform device discovery** and does not use the `BLUETOOTH_SCAN` permission; only devices already paired in Android settings are listed. The data received stays on the device, is used only for calculations and, optionally, saved with the measurement. **Nothing is transmitted to third parties.**
- **Beta status:** The feature is marked as Beta within the app. This does not change the data handling described above — no additional information is collected because of the testing stage.

### 2.4 Internet Access (Map Tiles)

- **What is accessed:** The app makes HTTP requests to the **OpenStreetMap** tile network (OpenTopoMap) to display the relief map on the viewing screen.
- **Purpose:** To render the background map on which the survey outline is plotted.
- **Data sent:** Only the geographic coordinates of the tiles needed to render the visible area — generic geographic position information, without identifying the user.
- **When it is accessed:** Only when the user navigates to the "Map" tab within a measurement or in the history.
- **Caching:** osmdroid may store tiles in a local cache to improve performance. This cache contains only map images, with no personal data of the user.

### 2.5 Point Names and Labels (from version 4.0)

- **What is accessed:** Optional text the user types to identify a captured point (e.g. "fence corner", "post 12").
- **Purpose:** To make points easier to recognise in the capture list, in the PDF report and in exported files.
- **Retention:** Stored together with the measurement, on the same terms as section 8.1. It is never sent to GHF Software servers or to Firebase.

### 2.6 Sending Feedback by Email (optional)

- **What happens:** On the external GNSS receiver screen, the "Send feedback" button opens the **user's own email app** with a pre-filled message addressed to `support@ghfsoftware.com`.
- **Data pre-filled in the message:** TopoWalk version, Android version and device manufacturer/model. No coordinates, measurements or history data are included.
- **User control:** The message is only sent if the user decides to send it, and they may edit or delete any part of the text beforehand. TopoWalk sends nothing automatically and has no access to the user's email account.
- **What we receive:** By choosing to send it, the user discloses to us the email address used, together with the content of the message. These emails are used exclusively to reply and to fix problems with the feature, are not shared with third parties or used for marketing, and can be deleted on request to the same address.

### 2.7 Orientation Sensors — Compass (from version 4.1)

- **What is accessed:** Readings from the device's rotation vector sensor (which Android composes from the magnetometer, accelerometer and gyroscope), to determine where the device is pointing.
- **Purpose:** Exclusively to draw the arrow on the **Stake-out** screen, which guides the user to a previously surveyed point. The correction between magnetic north and true north is calculated on the device itself, from the current position and Android's geomagnetic model.
- **When it is accessed:** Only while the Stake-out screen is open. The sensor is switched off when leaving it.
- **Retention:** The readings exist only in memory, while the screen is in use. **Nothing is stored or transmitted.** Devices without a compass simply do not show the arrow — the feature falls back to showing the numeric azimuth.

### 2.8 Report Branding (from version 4.1)

This is the only part of TopoWalk in which the user enters data **about themselves or their company**. It deserves careful reading.

- **What the user may enter:** company name, name of the technical lead, professional registration (CREA, CAU or equivalent), a free-text footer note, a colour and an image file to serve as a logo.
- **Purpose:** To compose the header and footer of the PDF reports generated by the user, so that the document delivered to their client carries the identity of the user's company, not that of the app.
- **How the logo is obtained:** through Android's own file picker (Storage Access Framework). The app **does not request storage permission** and **cannot see any file** other than the single one the user chooses. The image is resized and copied to the app's private area; the original file stays where it was and is not modified.
- **Where this data is kept:** exclusively on the device, in the app's local preferences and in its private file area. **It is never sent to GHF Software, Firebase, Google Play or any third party.** It does not appear in any analytics event or crash report.
- **When this data leaves the device:** only when the **user themselves** shares a PDF report — because it is a visible part of the document, which is precisely the purpose of the feature. The destination of that sharing is chosen by the user and is outside the app's control (same terms as section 8.2).
- **How to remove it:** the "Report branding" screen lets the user delete the logo and clear each field at any time. Clearing the app's data also removes everything.

### 2.9 Imported Files — Reference Layers (from version 4.2)

- **What is accessed:** a single file at a time, chosen by the user in Android's own picker (Storage Access Framework), in KML, KMZ, GeoJSON, GPX or CSV format. The app **does not request storage permission** and **cannot see any file** other than the one the user selects.
- **Purpose:** to display the perimeter or the points in the file as a reference layer on the map, and to allow walking to those points using the Stake-out screen. This is the case for someone who already has the KML from the CAR (Rural Environmental Registry), from SIGEF (the Brazilian federal land-registry georeferencing system) or a file sent by a client.
- **What the file may contain:** coordinates and point names chosen by whoever created the file. This content may be data about a property — and that is why it deserves this section.
- **Where it is kept:** the content is copied to the **app's private area, on the device itself** (the original file stays where it was and is not modified). The copy exists because the permission granted for the chosen file expires, and without it the layer would disappear by itself after some time.
- **Where it does not go:** imported content is **never sent** to GHF Software, Firebase, Google Play or any third party. It does not appear in any analytics event or crash report — the only thing recorded is that an import took place, in which format and with how many points, without any coordinates.
- **How to remove it:** the "Imported layers" screen lets the user remove each layer at any time; removing it deletes the internal copy and does not touch the original file. Clearing the app's data also removes everything.

### 2.10 Field Photos (from version 4.2)

This section describes the **only data in the app that may contain images of people or of property**, and it deserves careful reading.

- **What the user may attach:** up to 5 photos per survey, taken on the spot with the camera or chosen from the device's gallery.
- **Purpose:** to document the field — the survey marker, the gate, the erosion — together with the corresponding survey, and optionally to include them in the PDF report that the user delivers to their client.
- **The app does NOT request camera or storage permission.** A photo taken on the spot goes through the system's own camera app (`ACTION_IMAGE_CAPTURE`), and choosing from the gallery goes through Android's photo picker — in both cases the app receives only the file the user selected, and **cannot see any other photo on the device**.
- **Where they are kept:** the app makes a **reduced copy** (at most 1280 px, JPEG) in its private area, on the device itself. The original photo stays where it was and is not modified. The copy exists because the temporary address returned by the camera or the gallery expires, and without it the photo would disappear from the survey after some time.
- **Metadata:** the copy is saved **without the original's EXIF metadata** — which includes the geolocation that phone cameras usually record. Only the orientation is preserved, applied directly to the image so that the photo does not appear sideways in the report. In practice, the copy kept by TopoWalk carries **less** information than the original file.
- **Where they do not go:** photos are **never sent** to GHF Software, Firebase, Google Play or any third party. They do not appear in any analytics event or crash report — the only thing recorded is that an attachment was made and how many photos the survey now has, without any image and without any file name.
- **When they leave the device:** only when the **user themselves** shares a PDF report that includes them — because they are a visible part of the document, which is the purpose of the feature. The destination is chosen by the user and is outside the app's control (same terms as section 8.2).
- **How to remove them:** each photo can be removed individually on the survey screen. Deleting the survey deletes its photos along with it. Clearing the app's data removes everything. In none of these cases is the original file in the gallery touched.

### 2.11 Migrating TopoWalk Pro to the Google account (from version 4.3)

Anyone who already used TopoWalk before Pro existed received access free of charge (section 6). That
grant is recorded **on the device**, and so it would not follow a change of phone on its
own. This feature solves that: the user obtains a **Google Play promotional code**,
redeems it in the Play Store, and access then belongs to **their Google account**.

It is the **only** TopoWalk feature that stores anything on a server operated by GHF Software, and
it exists for a **limited time** — once the migration ends, the service is switched off and the data below
is deleted.

**Deadline:** the code can be requested until **31 March 2027**. After that date the
service is permanently switched off and all records described in this section are deleted.

- **When it happens:** only when the user opens the "Move Pro to your account" screen and
  taps to request the code. Anyone who never opens that screen **makes no connection at all** to
  our server: the app does not start a session, does not generate an identifier and does not send anything.
- **What is sent and stored:**
  - A **scrambled device identifier** (SHA-256 hash). The original identifier
    **is not sent** and cannot be recovered from what we store.
  - An **anonymous session identifier** generated by Firebase — a random number, with no
    name, no email and no password. It is not an account and does not require registration.
  - The **date and time** of the request and the **promotional code** delivered.
- **What is NOT sent:** name, email, Google account, payment data, location,
  surveys, photos or any content produced in the app.
- **What the scrambled identifier is for:** Google limits the codes to a
  fixed quantity per quarter. Without a way to recognise that a given device has already been
  served, repeated requests would exhaust the supply and leave those who are entitled without a code.
  It serves **only** that purpose: delivering one code per device.
- **Integrity check:** the request is accompanied by a **Google Play
  Integrity** attestation, which confirms to our server that the call comes from the
  genuine TopoWalk app, installed from the Play Store. This check is performed by Google and **reveals
  nothing about the user to us**.
- **Where it is kept:** Cloud Firestore and Cloud Functions, hosted on Google Cloud, under a
  GHF Software account.
- **For how long:** until **31 March 2027**, the deadline for requesting a code.
  Once the campaign ends, the records are exported for verification and deleted, and the service
  is switched off.
- **How to request deletion:** write to `support@ghfsoftware.com` stating the code you
  received. We delete the corresponding record.

---

## 3. Data NOT Collected

TopoWalk **does not collect, does not store remotely and does not transmit**:

- Name, email or any personal identification data — including in the Pro migration service (section 2.11), which **does not require login and does not receive any name or email**
- IP address or network data beyond what is needed to load map tiles and to send analytics events and crash reports
- Background location or location history outside active use of the app
- Advertising ID (the app explicitly removes this permission)

Three clarifications for accuracy:

1. **Feedback by email.** If the user voluntarily writes to us using the "Send feedback" button (section 2.6), we come to know the email address they chose to use and the content they wrote. This always depends on an explicit action by the user and does not occur in any other flow of the app.
2. **TopoWalk Pro migration (section 2.11).** This feature sends our server a scrambled device identifier and an anonymous session identifier. Neither of them carries a name, email or account, and neither is used outside that purpose. It is the **only** situation in which the app stores anything on a server of ours.
3. **Report branding (from version 4.1).** The user may type their own name and professional registration so that they appear in the PDF (section 2.8). This data **is personal**, but it stays **only on the user's device**: GHF Software does not receive it, does not store it and has no way of accessing it. It only leaves the device inside a PDF that the user themselves decides to share.

---

## 4. Analytics — Firebase Analytics (Google)

From version 3.10, TopoWalk uses **Firebase Analytics**, a usage analytics service provided by Google LLC.

### What is collected and sent to Firebase:

- **In-app interactions:** screens viewed, features used (e.g. point capture, file export, history access) and navigation flow.
- **Interest in future formats (version 4.0):** the export menu lists DXF and CSV as planned formats; tapping them does not generate any file, it only records an anonymous event (that the format was seen and, if the user taps a confirmation button within the screen, that they are interested in it). **No contact details are collected in this flow** — the app does not ask for an email or phone number, and there is no waiting list. This measurement **ends in version 4.1**, when both formats actually become available.
- **Purchase funnel (from version 4.1):** anonymous events recording that the purchase screen was opened, from which feature it was opened, that a purchase was started, and whether it was completed, cancelled or failed. **The price, currency, payment method and any identifier of the Google account or the payment method are not recorded** — only the step of the flow. They serve to find out whether the purchase screen is understandable, not to identify who bought.
- **Firebase installation ID:** an anonymous identifier generated by the SDK to aggregate sessions. It does not personally identify the user and can be reset by uninstalling and reinstalling the app.
- **Device information:** model, operating system version and language — collected automatically by the SDK to segment reports.

### What is NOT collected by Firebase:

- GPS coordinates or topographic measurement data
- Name, email or any personal information entered in the app
- Advertising ID (explicitly removed from the app)

### Purpose:

The data is used exclusively to understand how users interact with the app, to identify the most-used features and to guide future improvements. It is not used for advertising or personalisation.

### Retention and control:

Events remain available for our analysis for the retention period configured in the Google Analytics property — **at most 14 months** — and are then deleted from detailed analyses; aggregated data (counts, without identifiers) may remain in reports. Google also processes them in accordance with the [Google Privacy Policy](https://policies.google.com/privacy). The user can clear the Firebase installation ID by uninstalling the app.

---

## 5. Crash Reports — Firebase Crashlytics (Google)

From version 3.13, TopoWalk uses **Firebase Crashlytics**, a Google LLC service for crash reporting. It exists to detect problems that the user cannot report on their own — in particular connection failures with the external GNSS/RTK receiver, which occur in the field and without a useful error message.

### What is collected and sent to Crashlytics:

- **App crashes:** exception type, stack trace and thread state at the time of the error.
- **Non-fatal failures of the external receiver:** reason for disconnection, original Bluetooth exception, reconnection attempt number and an excerpt of up to 16 characters from the start of the receiver's data stream — deliberately short so that it contains only the sentence header (type and time), never coordinates.
- **Technical session context:** whether the external receiver is enabled, model name of the paired receiver, connection state, fix quality (e.g. `RTK_FIXED`), number of satellites and HDOP.
- **Purchase and logo-reading failures (from version 4.1):** the error code returned by Google Play when a purchase acknowledgement is not accepted, and the stack trace of an image that could not be read as a logo. **Neither contains the image content, the company data, the price or any account identifier.**
- **Device information and Firebase installation ID:** collected automatically by the SDK, on the same terms as section 4.

### What is NOT collected by Crashlytics:

- GPS coordinates, altitudes or any of the user's measurement data
- Names, notes or exported files of surveys
- Name, email or any personal information entered in the app
- Logo, company name, technical lead or professional registration (section 2.8)

### Purpose:

Exclusively to diagnose and fix defects in the app. The data is not used for advertising, personalisation or profiling.

### Retention and control:

Crash reports are kept by Crashlytics for **90 days** and then deleted, in accordance with the [Firebase privacy documentation](https://firebase.google.com/support/privacy) and the [Google Privacy Policy](https://policies.google.com/privacy).

---

## 6. In-App Purchases — Google Play Billing (from version 4.1)

From version 4.1, TopoWalk offers a **single, permanent purchase** (TopoWalk Pro), processed by **Google Play Billing**, a Google LLC service.

### Who processes the payment

**Payment is processed entirely by Google.** TopoWalk **never** sees, receives or stores card numbers, bank details, billing addresses or any payment information. That screen belongs to Google Play, not to the app, and what happens on it is governed by the [Google Privacy Policy](https://policies.google.com/privacy) and by the Google Play Terms of Service.

### What the app sends to Google Play

- The product identifier (`topowalk_pro`), to look up the price and open the purchase screen.
- An acknowledgement that the purchase was received (required by Google; without it the purchase is automatically refunded within three days).

The app **does not send any account, user or device identifier created by us** to Google Play. The feature Google offers to associate a purchase with a developer's internal account (`obfuscatedAccountId`) **is not used**.

TopoWalk **has no user accounts**: there is no registration, login, password or profile. The Pro migration service (section 2.11) uses an anonymous Firebase session, which is a random identifier generated by the device itself — it is not an account, does not ask for credentials and does not store any name or email.

### What the app receives and stores

- **The price already formatted** in the user's currency, to display on screen. The app does not know the currency or the country — it receives the ready-made text from Google.
- **Whether or not there is an active purchase** for the device, checked each time the app is opened. This answer is stored locally as a simple "yes or no", so that the app does not flash "not purchased" while it checks. **No Google account data is stored.**

### Why the check is repeated

The check happens every session because that is how a **refund** reaches the app: if the user asks Google for their money back, the purchase no longer appears and access is removed. The opposite also applies — anyone who reinstalls the app gets access back without paying again.

### Access granted without purchase

Users who already had TopoWalk installed before the launch of TopoWalk Pro receive access **free of charge and permanently**. This grant is recorded **only on the device**, and does not involve Google Play, a user account or any personal data.

Because it is recorded on the device, it would not follow a change of phone on its own. To solve this, the app offers the **Pro migration** described in section 2.11: the user obtains a promotional code, redeems it in the Play Store, and access then belongs to their Google account — coming back by itself on any device where they sign in with the same account.

### Minors

Purchases on Google Play are subject to Google Play's own parental controls and authentication requirements. TopoWalk does not implement its own age verification and has no way of knowing the age of the buyer.

---

## 7. Sharing Data with Third Parties

TopoWalk shares data with the following third parties:

| Third party | Data shared | Purpose |
|---|---|---|
| **Google LLC (Firebase Analytics)** | In-app interactions, installation ID, device information | Usage analytics |
| **Google LLC (Firebase Crashlytics)** | Stack traces, external receiver failures, technical session context, installation ID, device information | Crash diagnosis |
| **OpenStreetMap / OpenTopoMap** | Coordinates of the requested map tiles | Map rendering |
| **Google LLC (Google Play Billing)** — from version 4.1 | Product identifier and purchase acknowledgement. No account identifier created by us; no payment data passes through the app | Processing the TopoWalk Pro purchase |
| **Google LLC (Firebase Authentication)** — Pro migration, section 2.11 | An **anonymous** session: a random identifier generated by the device. No name, no email, no password | Identifying the call to our migration service |
| **GHF Software (Cloud Firestore and Cloud Functions, hosted on Google Cloud)** — Pro migration, section 2.11 | Scrambled device identifier, anonymous session identifier, date and time of the request and the promotional code delivered | Delivering one code to each user and preventing the supply from being exhausted by repeated requests |

The app does not integrate advertising SDKs, social networks or any other external service beyond those listed above.

---

## 8. Local Storage

### 8.1 Database (Measurement History)

When the user chooses to save a measurement, the following data is stored **locally on the device** in a Room (SQLite) database, accessible only by the app:

- Name and notes entered by the user
- Coordinates (latitude, longitude, altitude) of each point of the measurement
- Calculated results (distances, height differences, angles, area)
- Date and time of the measurement

This data is **never sent to GHF Software servers** and remains on the device until the user deletes it manually through the app or clears the app's data. See section 8.4 on the manual backup that TopoWalk itself offers, and section 8.5 on Android's system automatic backup — the two are independent of each other.

### 8.2 PDF Reports

When a PDF report is requested, the app:

1. Creates the PDF file temporarily in the app's **private cache directory** (`cacheDir`), accessible only by the app itself.
2. Shares the file via `FileProvider` with the app of your choice (WhatsApp, email, Google Drive, etc.) using Android's standard mechanism.
3. The file remains in the cache until it is deleted: the app removes export files older than 24 hours with each new DXF, CSV, GeoJSON, KML or GPX export, and the operating system may also clear the cache automatically. The user can also clear the app's data.

TopoWalk has no access to the destination chosen by the user for sharing — that operation is managed entirely by the Android system and by the receiving app.

### 8.3 File Export

The user can export measurements in **GeoJSON, KML and GPX** (from version 4.0) and in **DXF and CSV** (from version 4.1). These files are generated locally in the device's cache and shared in the same way as the PDF (section 8.2), including how long they remain in the cache: files older than 24 hours are deleted by the app at the next export. The app has no access to the sharing destination.

CSV export generates **two files** — one with the points and the other with the segments — shared together. In addition to the geometry, the DXF contains the latitude and longitude of the first point of the survey, written as text inside the file so that the drawing can be positioned; this is the same coordinate data that the other formats already carry.

### 8.4 History Backup and Restore (from version 4.0)

TopoWalk allows the user to manually export **the entire measurement history** to a single file, and restore it later — on the same device, after reinstallation, or on another device.

- **How it works:** when the user taps "Back up history", the app uses Android's own file picker (Storage Access Framework) so that the user chooses where to save the file — Google Drive, memory card, internal storage or any other location listed by the system. **The app writes directly to the location chosen by the user**, without going through the app-to-app share sheet used for the PDF and the other formats (sections 8.2 and 8.3), and without sending the file to GHF Software servers.
- **What the file contains:** name, notes, coordinates, altitude, calculated results and point labels of each saved measurement — the same data already described in section 8.1, gathered into a single file.
- **Restoring:** when the user chooses "Restore backup" and selects a file (through the same system picker), the measurements in the file are added to the device's history. Nothing already saved is deleted, and measurements that already exist are identified and not duplicated. A file generated by a newer version of TopoWalk than the one installed is rejected, so as not to corrupt the local database.
- **User control:** GHF Software has no access to this file at any time — it exists only in the location that the user chose when saving it, under their control and responsibility (including the security of their own Google Drive account, if that is the chosen destination).

This mechanism is independent of Android's system Automatic Backup, described in section 8.5.

### 8.5 Android System Automatic Backup

TopoWalk **does not operate any cloud backup or synchronisation service of its own**. However, the app does not disable **Android Auto Backup** ("Backup by Google"), which is a mechanism of the operating system itself, independent of TopoWalk:

- If the user has this feature enabled in their Google account (it is the factory default on most Android devices) and the device meets the conditions defined by Android itself (connected to Wi-Fi, charging and idle), the operating system may, periodically and in the background, include TopoWalk's data — including the local measurement history database — in the backup of the user's Google account.
- This backup is stored and managed by **Google's infrastructure**, associated with the user's own Google account — GHF Software has no access to this backup, does not receive it, does not control it and cannot delete it.
- If the user reinstalls TopoWalk on the same device or on another device signed in to the same Google account, Android may automatically restore this data from that backup.
- Users who do not want the measurement history to be included in this system backup can turn off "Backup by Google" for the device, or for TopoWalk specifically, in Android settings (Settings → System → Backup, depending on the manufacturer and the Android version).

**Note regarding report branding (section 2.8):** the copied logo and the company data are kept in the app's private area and preferences, and may therefore also be included in this system automatic backup — in the user's own Google account, always beyond the reach of GHF Software. Anyone who does not want this can turn off the system backup as described above.

This section describes Android's default behaviour for data management. It does not change any other commitment in this policy: GHF Software still does not operate its own servers for storing user data and has no access to this content at any time.

### 8.6 Data off the device (Pro migration)

All the rest of section 8 describes storage **on the device itself**. The only exception in the
app is the Pro migration service (section 2.11), which stores on a GHF Software server
a scrambled device identifier, an anonymous session identifier, the date of the request
and the code delivered — nothing more, and nothing that identifies the person. Surveys, photos and
reports **never** leave the device by this route.

---

## 9. App Permissions

| Permission | Reason |
|---|---|
| `ACCESS_FINE_LOCATION` | Obtain precise GPS coordinates for the measurement points |
| `ACCESS_COARSE_LOCATION` | Complementary permission required by Android for location |
| `INTERNET` | Load map tiles from OpenStreetMap, send events to Firebase Analytics and crash reports to Crashlytics and, **when the user requests the Pro migration** (section 2.11), communicate with our server |
| `VIBRATE` | Haptic feedback when capturing a measurement point |
| `BLUETOOTH_CONNECT` (Android 12+) | Connect to an already-paired external GNSS/RTK receiver, when the feature is enabled by the user |
| `BLUETOOTH` / `BLUETOOTH_ADMIN` (Android 11 and earlier) | Equivalent for older Android versions for the same connection |
| `com.android.vending.BILLING` (from version 4.1) | Required by Google Play to offer the TopoWalk Pro purchase. It is added automatically by Google's library and **does not give access to any data on the device** |

**The compass used in Stake-out (section 2.7) and choosing the logo (section 2.8) do not require any permission:** orientation sensors are freely available on Android, and the file picker gives the app only the single file the user chooses.

The app does not request access to the microphone, contacts or external storage. **Nor does it request camera permission** — field photos (section 2.10) come in through the system camera app and Android's photo picker, which give TopoWalk only the file chosen by the user. The advertising ID (`AD_ID`) is explicitly removed from the app and is not collected.

---

## 10. Use by Minors

TopoWalk is not directed at children under 13 and does not knowingly collect data from minors. In the European Union, anyone under 16 (or the minimum age set by their country, between 13 and 16) should only use the app with the authorisation of their legal guardian. As it is a technical field tool, use by minors should take place under the supervision of a responsible adult.

From version 4.1, the purchase of TopoWalk Pro is processed by Google Play and is subject to that service's parental controls and authentication requirements (section 6). TopoWalk does not perform its own age verification.

---

## 11. Security

TopoWalk's measurement data is processed and stored exclusively on the user's device. Communication with external services (Firebase, Google Play and OpenStreetMap) takes place exclusively over HTTPS with encryption in transit. The data sent to Firebase does not contain names, emails, coordinates or survey content. The installation ID, the device information and the IP address seen by Google's servers are nevertheless treated by us as **personal data**, because that is how the LGPD and the GDPR classify them — and that is why sections 12 to 14 apply to them. The security of locally stored data is managed by the Android operating system and by app isolation (sandbox).

From version 4.1, **no payment data passes through the app**: the purchase is handled entirely through the Google Play screen, and TopoWalk receives back only the information on whether or not there is an active purchase (section 6).

---

## 12. Legal Bases for Processing

Each use of personal data described above has a legal basis under the LGPD (Art. 7) and the GDPR (Art. 6):

| Processing | Section | Legal basis |
|---|---|---|
| Location, barometer, compass and Bluetooth for calculations | 2.1 to 2.3, 2.7 | Performance of the service requested by the user (Art. 7(V) LGPD; Art. 6(1)(b) GDPR). This data does not leave the device |
| Typed data, photos, imported files, report branding | 2.5, 2.8 to 2.10 | Performance of the service requested by the user. It stays on the device |
| Map tiles (OpenStreetMap / OpenTopoMap) | 2.4 | Performance of the service requested by the user: the map only loads when they open the tab |
| Analytics (Firebase Analytics) | 4 | Legitimate interest in understanding usage and improving the app (Art. 7(IX) LGPD; Art. 6(1)(f) GDPR), without advertising, without profiling and without survey data |
| Crash reports (Firebase Crashlytics) | 5 | Legitimate interest in detecting and fixing defects, including those the user cannot report |
| TopoWalk Pro purchase (Google Play Billing) | 6 | Performance of the purchase contract |
| Legacy Pro migration | 2.11 | Performance of the service requested by the user, which only takes place when they request the code; legitimate interest in preventing the limited supply of codes from running out |
| Feedback and support emails | 2.6 | Legitimate interest in replying to those who write to us |

Where the legal basis is legitimate interest, the user may **object** to the processing (section 13).

---

## 13. Your Rights

Under the LGPD (Art. 18) and the GDPR (Arts. 15 to 22), you may request:

- **Access and confirmation:** to know whether we process your data and what it is.
- **Rectification** of incorrect data.
- **Erasure** of the data we process.
- **Portability:** surveys can already be taken to another device or program through the backup (section 8.4) and the exports (section 8.3), without asking us for anything.
- **Objection** to processing based on legitimate interest (analytics and crash reports).
- **Restriction** of processing while a request of yours is being assessed.
- **Information** about with whom the data is shared (section 7).

**How to exercise them:** write to **support@ghfsoftware.com**. We reply within 15 days and, at most, within the period set by the applicable law (one month under the GDPR).

**A practical limitation, stated frankly:** TopoWalk has no account or login, and therefore **we do not know who you are**. Analytics and crash data are linked only to the device's installation ID, which we cannot associate with a person on the basis of an email address. For us to locate your records, the request needs to include something that identifies them (for example, the promotional code received in the Pro migration). Without that, the most direct way to stop all sending is to **uninstall the app**: the installation ID ceases to exist, and the data already sent expires within the periods in sections 4 and 5. The data on the device (surveys, photos, report branding) you can delete yourself, at any time, through the app itself or by clearing the app's data.

**Complaint to an authority:** you may lodge a complaint with the **Autoridade Nacional de Proteção de Dados (ANPD — Brazilian National Data Protection Authority)**, in Brazil, or with the data protection authority of the European Union country where you live or work — preferably after talking to us, so that we can resolve it first.

---

## 14. International Data Transfers

The Google services used by the app (Firebase Analytics, Crashlytics, Authentication, Cloud Firestore, Cloud Functions and Google Play) may process data on servers outside your country, including in the United States. Google LLC participates in the **EU-U.S. Data Privacy Framework** and adopts the **standard contractual clauses** approved by the European Commission, which are the mechanisms provided for in the GDPR (Arts. 45 and 46) and in the LGPD (Art. 33) for such transfers. Map tiles come from OpenTopoMap's servers.

Surveys, photos and reports are not part of any transfer: they stay on the device (section 8).

---

## 15. Changes to this Policy

We may update this Privacy Policy from time to time. Relevant changes will be announced through a new version of the app published on the Google Play Store. The "Last updated" date at the top of this document will always reflect the version in force.

We recommend that you review this policy periodically.

---

## 16. Contact

Questions, requests or comments about this Privacy Policy, and the requests in section 13, can be sent to:

**GHF Software** — ‹fill in: full name›, ‹fill in: city/state›, Brazil\
Email: **support@ghfsoftware.com**

---

*This policy was prepared in accordance with the Lei Geral de Proteção de Dados (LGPD — Brazilian General Data Protection Law, Law No. 13,709/2018), the European Union General Data Protection Regulation (GDPR — Regulation (EU) 2016/679) and the Google Play Store privacy policies. The [Portuguese version](PRIVACY_POLICY.md) is the reference version, and this English text is a translation; in case of discrepancy the Portuguese text prevails, without prejudice to rights that the law of your country grants you. See also the [Terms of Use](TERMS_OF_USE.en.md).*
