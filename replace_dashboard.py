import re

with open("src/AppUI/Dashboard.java", "r") as f:
    code = f.read()

# 1. Rooms
rooms_fn = """    private static ScrollPane createRoomsContent() {
        VBox main = new VBox(25);
        main.getStyleClass().add("card-container");
        
        // Large Top Header
        HBox topBox = new HBox(15);
        topBox.setAlignment(Pos.CENTER_LEFT);
        
        VBox titleBox = new VBox(5);
        Label rTitle = new Label("Rooms");
        rTitle.setStyle("-fx-font-size: 28px; -fx-font-weight: bold; -fx-text-fill: #0f172a;");
        Label rSub = new Label("Manage your hostel rooms and availability");
        rSub.setStyle("-fx-font-size: 14px; -fx-text-fill: #64748b;");
        titleBox.getChildren().addAll(rTitle, rSub);
        
        Region spacer1 = new Region(); HBox.setHgrow(spacer1, Priority.ALWAYS);
        Button addRoom = new Button("+ Add Room");
        addRoom.setStyle("-fx-background-color: #2563eb; -fx-text-fill: white; -fx-font-weight: bold; -fx-font-size: 14px; -fx-padding: 10 24; -fx-background-radius: 8; -fx-cursor: hand;");
        addRoom.setOnAction(e -> showAddRoomDialog());
        
        topBox.getChildren().addAll(titleBox, spacer1, addRoom);

        // Filter Bar
        HBox filterBar = new HBox(15);
        filterBar.setAlignment(Pos.CENTER_LEFT);
        filterBar.setStyle("-fx-background-color: white; -fx-padding: 8 15; -fx-background-radius: 8; -fx-border-color: #e2e8f0; -fx-border-radius: 8; -fx-border-width: 1;");
        
        Label searchIcon = new Label("🔍"); searchIcon.setStyle("-fx-text-fill: #94a3b8;");
        TextField search = new TextField();
        search.setPromptText("Search by room number...");
        search.setStyle("-fx-background-color: transparent; -fx-font-size: 14px; -fx-text-fill: #334155;");
        HBox.setHgrow(search, Priority.ALWAYS);
        
        Label filterIcon = new Label("Y"); filterIcon.setStyle("-fx-text-fill: #94a3b8; -fx-font-size: 16px; -fx-font-family: 'monospace';");
        ComboBox<String> filterCombo = new ComboBox<>();
        filterCombo.getItems().addAll("All Status", "Occupied", "Available");
        filterCombo.setValue("All Status");
        filterCombo.setStyle("-fx-background-color: transparent; -fx-font-size: 14px; -fx-text-fill: #334155; -fx-cursor: hand;");
        
        filterBar.getChildren().addAll(searchIcon, search, filterIcon, filterCombo);

        FlowPane flow = new FlowPane(25, 25);
        flow.setAlignment(Pos.CENTER_LEFT);

        search.textProperty().addListener((obs, oldV, newV) -> renderRoomsGrid(flow, newV, filterCombo.getValue()));
        filterCombo.valueProperty().addListener((obs, oldV, newV) -> renderRoomsGrid(flow, search.getText(), newV));

        renderRoomsGrid(flow, "", "All Status");

        main.getChildren().addAll(topBox, filterBar, flow);
        ScrollPane sp = new ScrollPane(main);
        sp.setFitToWidth(true); sp.setStyle("-fx-background: transparent; -fx-background-color: transparent;");
        return sp;
    }

    private static void renderRoomsGrid(FlowPane flow, String searchText, String statusFilter) {
        flow.getChildren().clear();
        List<Room> rooms = RoomDAO.getAllRooms();
        
        for (Room r : rooms) {
            String lowerSearch = searchText.toLowerCase();
            if (!r.getName().toLowerCase().contains(lowerSearch)) continue;
            
            String status = r.getStatus() != null ? r.getStatus().toLowerCase() : "available";
            if (!statusFilter.equals("All Status") && !status.equalsIgnoreCase(statusFilter)) continue;
            
            VBox card = new VBox(20);
            card.setStyle("-fx-background-color: white; -fx-background-radius: 8; -fx-border-radius: 8; -fx-border-width: 1; -fx-border-color: #e2e8f0; -fx-padding: 30; -fx-effect: dropshadow(gaussian, rgba(0,0,0,0.01), 5, 0, 0, 1);");
            card.setPrefWidth(260);

            boolean isOcc = "occupied".equals(status);
            HBox header = new HBox(12);
            header.setAlignment(Pos.CENTER_LEFT);
            Label rName = new Label("Room " + r.getName());
            rName.setStyle("-fx-font-size: 20px; -fx-font-weight: 800; -fx-text-fill: #0f172a;");
            
            Label rStatus = new Label(status);
            rStatus.setStyle("-fx-font-size: 11px; -fx-font-weight: 600; -fx-padding: 5 10; -fx-background-radius: 12;");
            if (isOcc) {
                rStatus.setStyle(rStatus.getStyle() + "; -fx-background-color: #dbeafe; -fx-text-fill: #2563eb;");
            } else {
                rStatus.setStyle(rStatus.getStyle() + "; -fx-background-color: #d1fae5; -fx-text-fill: #10b981;");
            }
            Region spHead = new Region(); HBox.setHgrow(spHead, Priority.ALWAYS);
            header.getChildren().addAll(rName, spHead, rStatus);
            
            Label rType = new Label(r.getType() != null ? r.getType() : "Dormitory");
            rType.setStyle("-fx-text-fill: #64748b; -fx-font-size: 13px; -fx-font-weight: 500;");

            VBox props = new VBox(12);
            props.setPadding(new Insets(10, 0, 10, 0));
            props.getChildren().addAll(
                createPropRow("Capacity", r.getCapacity().replace(" beds", "") + " beds"),
                createPropRow("Occupied", r.getOccupied().replace(" /", " /")),
                createPropRow("Price per night", r.getPrice().replace("Rs. ", "$")) // Updated label
            );
            
            double progress = 0;
            try {
                int occ = Integer.parseInt(r.getOccupied().split("/")[0].trim());
                int cap = Integer.parseInt(r.getOccupied().split("/")[1].trim());
                if (cap > 0) progress = (double) occ / cap;
            } catch (Exception ignore) {}
            
            HBox progTrack = new HBox();
            progTrack.setStyle("-fx-background-color: #e2e8f0; -fx-background-radius: 4; -fx-pref-height: 8;");
            HBox progFill = new HBox();
            progFill.setStyle("-fx-background-color: #2563eb; -fx-background-radius: 4; -fx-pref-height: 8;");
            progFill.prefWidthProperty().bind(card.widthProperty().subtract(60).multiply(progress));
            StackPane progPane = new StackPane(progTrack, progFill);
            StackPane.setAlignment(progFill, Pos.CENTER_LEFT);

            Button viewBtn = new Button("View Details");
            viewBtn.setStyle("-fx-background-color: white; -fx-border-color: #e2e8f0; -fx-text-fill: #334155; -fx-border-radius: 8; -fx-background-radius: 8; -fx-padding: 10; -fx-font-weight: bold; -fx-cursor: hand; -fx-pref-width: 250;");
            viewBtn.setOnAction(e -> {
                 if (confirmDelete("room", r.getName())) {
                     RoomDAO.deleteRoom(r.getId());
                     renderRoomsGrid(flow, searchText, statusFilter);
                 }
            });

            if (isOcc) {
                card.getChildren().addAll(header, rType, props, progPane, viewBtn);
            } else {
                card.getChildren().addAll(header, rType, props, viewBtn);
            }
            flow.getChildren().add(card);
        }
    }"""

guests_fn = """    private static ScrollPane createGuestsContent() {
        VBox main = new VBox(25);
        main.getStyleClass().add("card-container");

        HBox topBox = new HBox(15);
        topBox.setAlignment(Pos.CENTER_LEFT);
        VBox titleBox = new VBox(5);
        Label gTitle = new Label("Guests");
        gTitle.setStyle("-fx-font-size: 28px; -fx-font-weight: bold; -fx-text-fill: #0f172a;");
        Label gSub = new Label("Manage guest information and stays");
        gSub.setStyle("-fx-font-size: 14px; -fx-text-fill: #64748b;");
        titleBox.getChildren().addAll(gTitle, gSub);
        
        Region spacer1 = new Region(); HBox.setHgrow(spacer1, Priority.ALWAYS);
        Button addGuest = new Button("+ Add Guest"); // Even though it might be hidden in screenshot, good to have it there or we can match rooms
        addGuest.setStyle("-fx-background-color: #2563eb; -fx-text-fill: white; -fx-font-weight: bold; -fx-font-size: 14px; -fx-padding: 10 24; -fx-background-radius: 8; -fx-cursor: hand;");
        addGuest.setOnAction(e -> showAddGuestDialog(""));
        topBox.getChildren().addAll(titleBox, spacer1, addGuest);

        HBox filterBar = new HBox(15);
        filterBar.setAlignment(Pos.CENTER_LEFT);
        filterBar.setStyle("-fx-background-color: white; -fx-padding: 8 15; -fx-background-radius: 8; -fx-border-color: #e2e8f0; -fx-border-radius: 8; -fx-border-width: 1;");
        
        Label searchIcon = new Label("🔍"); searchIcon.setStyle("-fx-text-fill: #94a3b8;");
        TextField search = new TextField();
        search.setPromptText("Search by name, email, or room number...");
        search.setStyle("-fx-background-color: transparent; -fx-font-size: 14px; -fx-text-fill: #334155;");
        HBox.setHgrow(search, Priority.ALWAYS);
        filterBar.getChildren().addAll(searchIcon, search);

        FlowPane flow = new FlowPane(25, 25);
        flow.setAlignment(Pos.CENTER_LEFT);
        search.textProperty().addListener((obs, oldV, newV) -> renderGuestsGrid(flow, newV));
        renderGuestsGrid(flow, "");

        main.getChildren().addAll(topBox, filterBar, flow);
        ScrollPane sp = new ScrollPane(main); sp.setFitToWidth(true); sp.setStyle("-fx-background: transparent; -fx-background-color: transparent;");
        return sp;
    }

    private static void renderGuestsGrid(FlowPane flow, String searchText) {
        flow.getChildren().clear();
        List<Guest> guests = GuestDAO.getAllGuests();
        
        for (Guest g : guests) {
            String searchL = searchText.toLowerCase();
            if (!g.getName().toLowerCase().contains(searchL) && !g.getRoom().toLowerCase().contains(searchL) && !(g.getEmail() != null && g.getEmail().toLowerCase().contains(searchL))) continue;
            
            VBox card = new VBox(15);
            card.setStyle("-fx-background-color: white; -fx-background-radius: 8; -fx-border-radius: 8; -fx-border-width: 1; -fx-border-color: #e2e8f0; -fx-padding: 30; -fx-effect: dropshadow(gaussian, rgba(0,0,0,0.01), 5, 0, 0, 1);");
            card.setPrefWidth(260);
            
            HBox header = new HBox(10);
            header.setAlignment(Pos.CENTER);
            
            Label initials = new Label(g.getInitials());
            initials.setStyle("-fx-background-color: #dbeafe; -fx-text-fill: #2563eb; -fx-font-size: 20px; -fx-font-weight: 500; -fx-min-width: 60; -fx-min-height: 60; -fx-background-radius: 30; -fx-alignment: center;");
            
            Region spHead = new Region(); HBox.setHgrow(spHead, Priority.ALWAYS);
            
            VBox roomBox = new VBox(2);
            roomBox.setAlignment(Pos.CENTER_RIGHT);
            Label rLbl = new Label("Room"); rLbl.setStyle("-fx-text-fill: #64748b; -fx-font-size: 13px;");
            Label rVal = new Label(g.getRoom()); rVal.setStyle("-fx-font-size: 18px; -fx-font-weight: bold; -fx-text-fill: #0f172a;");
            roomBox.getChildren().addAll(rLbl, rVal);
            
            header.getChildren().addAll(initials, spHead, roomBox);
            
            Label gName = new Label(g.getName());
            gName.setStyle("-fx-font-size: 20px; -fx-font-weight: bold; -fx-text-fill: #0f172a; -fx-padding: 10 0 0 0;");
            
            VBox contactBox = new VBox(8);
            contactBox.getChildren().addAll(
                createIconRow("📍", g.getLocation() != null ? g.getLocation() : "Unknown"),
                createIconRow("✉", g.getEmail() != null ? g.getEmail() : "No email"),
                createIconRow("📞", g.getPhone() != null ? g.getPhone() : "No phone")
            );
            
            VBox datesBox = new VBox(8);
            datesBox.setStyle("-fx-border-width: 1 0 0 0; -fx-border-color: #f1f5f9; -fx-padding: 15 0 0 0; -fx-margin: 5 0 5 0;");
            datesBox.getChildren().addAll(
                createPropRow("Check-in", g.getCheckIn()),
                createPropRow("Check-out", g.getCheckOut())
            );
            
            Button viewBtn = new Button("View Details");
            viewBtn.setStyle("-fx-background-color: white; -fx-border-color: #e2e8f0; -fx-text-fill: #334155; -fx-border-radius: 8; -fx-background-radius: 8; -fx-padding: 10; -fx-font-weight: bold; -fx-cursor: hand; -fx-pref-width: 250;");
            viewBtn.setOnAction(e -> {
                 if (confirmDelete("guest", g.getName())) {
                     GuestDAO.deleteGuest(g.getId());
                     renderGuestsGrid(flow, searchText);
                 }
            });
            
            card.getChildren().addAll(header, gName, contactBox, datesBox, viewBtn);
            flow.getChildren().add(card);
        }
    }
    
    private static HBox createIconRow(String icon, String text) {
        HBox r = new HBox(8);
        r.setAlignment(Pos.CENTER_LEFT);
        Label i = new Label(icon); i.setStyle("-fx-text-fill: #94a3b8; -fx-font-size: 14px;");
        Label t = new Label(text); t.setStyle("-fx-text-fill: #475569; -fx-font-size: 13px;");
        r.getChildren().addAll(i, t);
        return r;
    }"""

bookings_fn = """    private static ScrollPane createBookingsContent() {
        VBox main = new VBox(20);
        main.getStyleClass().add("card-container");
        
        HBox topBox = new HBox(15);
        topBox.setAlignment(Pos.CENTER_LEFT);
        
        VBox titleBox = new VBox(5);
        Label rTitle = new Label("Bookings");
        rTitle.setStyle("-fx-font-size: 28px; -fx-font-weight: bold; -fx-text-fill: #0f172a;");
        Label rSub = new Label("Manage reservations and check-ins");
        rSub.setStyle("-fx-font-size: 14px; -fx-text-fill: #64748b;");
        titleBox.getChildren().addAll(rTitle, rSub);
        
        Region spacer1 = new Region(); HBox.setHgrow(spacer1, Priority.ALWAYS);
        Button addBtn = new Button("+ New Booking");
        addBtn.setStyle("-fx-background-color: #2563eb; -fx-text-fill: white; -fx-font-weight: bold; -fx-font-size: 14px; -fx-padding: 10 24; -fx-background-radius: 8; -fx-cursor: hand;");
        addBtn.setOnAction(e -> showAddBookingDialog());
        topBox.getChildren().addAll(titleBox, spacer1, addBtn);
        
        HBox filterBar = new HBox(15);
        filterBar.setAlignment(Pos.CENTER_LEFT);
        filterBar.setStyle("-fx-background-color: white; -fx-padding: 8 15; -fx-background-radius: 8; -fx-border-color: #e2e8f0; -fx-border-radius: 8; -fx-border-width: 1;");
        
        Label searchIcon = new Label("🔍"); searchIcon.setStyle("-fx-text-fill: #94a3b8;");
        TextField search = new TextField();
        search.setPromptText("Search by guest name or room number...");
        search.setStyle("-fx-background-color: transparent; -fx-font-size: 14px; -fx-text-fill: #334155;");
        HBox.setHgrow(search, Priority.ALWAYS);
        
        Label filterIcon = new Label("Y"); filterIcon.setStyle("-fx-text-fill: #94a3b8; -fx-font-size: 16px; -fx-font-family: 'monospace';");
        ComboBox<String> filterCombo = new ComboBox<>();
        filterCombo.getItems().addAll("All Status", "Checked-in", "Pending", "Cancelled");
        filterCombo.setValue("All Status");
        filterCombo.setStyle("-fx-background-color: transparent; -fx-font-size: 14px; -fx-text-fill: #334155; -fx-cursor: hand;");
        
        filterBar.getChildren().addAll(searchIcon, search, filterIcon, filterCombo);
        
        VBox tableContainer = new VBox();
        tableContainer.setStyle("-fx-background-color: white; -fx-background-radius: 8; -fx-border-radius: 8; -fx-border-width: 1; -fx-border-color: #e2e8f0;");
        
        // Table Header
        HBox header = new HBox(10);
        header.setAlignment(Pos.CENTER_LEFT);
        header.setPadding(new Insets(15, 20, 15, 20));
        header.setStyle("-fx-border-width: 0 0 1 0; -fx-border-color: #e2e8f0; -fx-background-color: #f8fafc; -fx-background-radius: 8 8 0 0;");
        String headerStyle = "-fx-font-weight: 800; -fx-text-fill: #64748b; -fx-font-size: 12px;";
        Label hId = new Label("BOOKING\nID"); hId.setStyle(headerStyle); hId.setPrefWidth(80);
        Label hName = new Label("GUEST\nNAME"); hName.setStyle(headerStyle); hName.setPrefWidth(150);
        Label hRoom = new Label("ROOM"); hRoom.setStyle(headerStyle); hRoom.setPrefWidth(80);
        Label hIn = new Label("CHECK-IN"); hIn.setStyle(headerStyle); hIn.setPrefWidth(120);
        Label hOut = new Label("CHECK-\nOUT"); hOut.setStyle(headerStyle); hOut.setPrefWidth(120);
        Label hGuests = new Label("GUESTS"); hGuests.setStyle(headerStyle); hGuests.setPrefWidth(80);
        Label hStatus = new Label("STATUS"); hStatus.setStyle(headerStyle); hStatus.setPrefWidth(100);
        header.getChildren().addAll(hId, hName, hRoom, hIn, hOut, hGuests, hStatus);
        
        VBox list = new VBox();
        search.textProperty().addListener((obs, oldV, newV) -> renderBookingsList(list, newV, filterCombo.getValue()));
        filterCombo.valueProperty().addListener((obs, oldV, newV) -> renderBookingsList(list, search.getText(), newV));
        
        renderBookingsList(list, "", "All Status");
        
        tableContainer.getChildren().addAll(header, list);
        
        main.getChildren().addAll(topBox, filterBar, tableContainer);
        ScrollPane sp = new ScrollPane(main); sp.setFitToWidth(true); sp.setStyle("-fx-background: transparent; -fx-background-color: transparent;");
        return sp;
    }

    private static void renderBookingsList(VBox list, String searchText, String statusFilter) {
        list.getChildren().clear();
        List<Booking> bookings = BookingDAO.getAllBookings();
        
        for (int i = 0; i < bookings.size(); i++) {
            Booking b = bookings.get(i);
            String searchL = searchText.toLowerCase();
            if (!b.getGuestName().toLowerCase().contains(searchL) && !b.getRoom().contains(searchL)) continue;
            
            String status = b.getStatus() != null ? b.getStatus() : "checked-in";
            
            HBox row = new HBox(10);
            row.setPadding(new Insets(20, 20, 20, 20));
            row.setAlignment(Pos.CENTER_LEFT);
            if (i < bookings.size() - 1) {
                row.setStyle("-fx-border-width: 0 0 1 0; -fx-border-color: #e2e8f0;");
            }
            
            String txtStyle = "-fx-text-fill: #334155; -fx-font-size: 15px;";
            Label cId = new Label(b.getBookingId()); cId.setStyle(txtStyle); cId.setPrefWidth(80);
            
            VBox nameBox = new VBox();
            Label cName = new Label(b.getGuestName().split(" ")[0]); 
            Label cNameLast = new Label(b.getGuestName().substring(b.getGuestName().indexOf(" ") + 1));
            cName.setStyle("-fx-text-fill: #0f172a; -fx-font-size: 15px; -fx-font-weight: 500;"); 
            cNameLast.setStyle("-fx-text-fill: #0f172a; -fx-font-size: 15px; -fx-font-weight: 500;");
            nameBox.getChildren().addAll(cName, cNameLast);
            nameBox.setPrefWidth(150);
            
            Label cRoom = new Label(b.getRoom()); cRoom.setStyle(txtStyle); cRoom.setPrefWidth(80);
            
            String inDate = b.getCheckIn().replace("📅 ", "");
            String outDate = b.getCheckOut().replace("📅 ", "");
            
            Label cIn = new Label("📅 " + inDate.substring(0, 5) + "\\n   " + inDate.substring(5)); 
            cIn.setStyle("-fx-text-fill: #64748b; -fx-font-size: 14px;"); cIn.setPrefWidth(120);
            Label cOut = new Label("�� " + outDate.substring(0, 5) + "\\n   " + outDate.substring(5)); 
            cOut.setStyle("-fx-text-fill: #64748b; -fx-font-size: 14px;"); cOut.setPrefWidth(120);
            
            Label cGuests = new Label(b.getGuestsCount()); cGuests.setStyle(txtStyle); cGuests.setPrefWidth(80);
            
            Label statusView = new Label(status);
            statusView.setStyle("-fx-font-size: 12px; -fx-font-weight: 600; -fx-padding: 5 12; -fx-background-radius: 15;");
            if (status.equalsIgnoreCase("checked-in")) {
                statusView.setStyle(statusView.getStyle() + "; -fx-background-color: #d1fae5; -fx-text-fill: #10b981;");
            } else {
                statusView.setStyle(statusView.getStyle() + "; -fx-background-color: #f1f5f9; -fx-text-fill: #64748b;");
            }
            
            HBox sBox = new HBox(statusView); sBox.setPrefWidth(100);
            row.getChildren().addAll(cId, nameBox, cRoom, cIn, cOut, cGuests, sBox);
            list.getChildren().add(row);
        }
    }"""


# Replace logic
new_code = re.sub(
    r'    private static ScrollPane createRoomsContent\(\) \{.*?(?=    private static HBox createPropRow)',
    rooms_fn + "\n\n",
    code,
    flags=re.DOTALL
)

new_code = re.sub(
    r'    private static ScrollPane createGuestsContent\(\) \{.*?(?=    private static ScrollPane createPaymentsContent)',
    guests_fn + "\n\n",
    new_code,
    flags=re.DOTALL
)

new_code = re.sub(
    r'    private static ScrollPane createBookingsContent\(\) \{.*?(?=    private static boolean confirmDelete)',
    bookings_fn + "\n\n",
    new_code,
    flags=re.DOTALL
)

with open("src/AppUI/Dashboard.java", "w") as f:
    f.write(new_code)

print("Replacement complete.")
