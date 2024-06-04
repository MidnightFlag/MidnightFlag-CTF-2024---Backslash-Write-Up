// gcc letmebuy.c -o letmebuy -no-pie

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_USERS 10
#define MAX_SELLERS 1
#define MAX_USERNAME_LENGTH 20
#define MAX_PASSWORD_LENGTH 20
#define MAX_DESCRIPTION_LENGTH 22

////////////////////////////////////// Account Functions //////////////////////////////////////

typedef enum {
    BUYER,
    SELLER
} Role;
int num_sellers = 0;
int num_users = 1;

typedef struct {
    char username[MAX_USERNAME_LENGTH];
    char password[MAX_PASSWORD_LENGTH];
    char description[MAX_PASSWORD_LENGTH];
    Role role;
    int balance;
} User;

User users[MAX_USERS] = {
    {"owner", "", "I'm so rich", SELLER, 99999999},
};

User *current_user = NULL; // Utilisateur actuellement connecté

void login() {
    char username[MAX_USERNAME_LENGTH];
    char password[MAX_PASSWORD_LENGTH];

    printf("Enter your username:\n");
    fgets(username, MAX_USERNAME_LENGTH, stdin);
    strtok(username, "\n");
    
    printf("Enter your password:\n");
    fgets(password, MAX_PASSWORD_LENGTH, stdin);
    strtok(password, "\n");

    // Rechercher l'utilisateur
    for (int i = 0; i < num_users; i++) {
        if (strcmp(users[i].username, username) == 0 && strcmp(users[i].password, password) == 0) {
            printf("Login successful. Welcome, %s!\n", username);            
            current_user = &users[i]; // Utilisateur connecté
            return;
        }
    }
    printf("Login failed. Invalid username or password.\n");
}

void get_input(const char *prompt, char *buffer, int max_length) {
    printf("%s", prompt);
    fflush(stdin);
    fgets(buffer, max_length, stdin);
    buffer[strcspn(buffer, "\n")] = '\0'; // Supprime le \n
}

void create_account() {
    char username[MAX_USERNAME_LENGTH];
    int role_choice;

    if (num_users >= MAX_USERS) {
        printf("Maximum number of users reached.\n");
        return;
    }
    
    printf("Select account type:\n");
    printf("1. Buyer\n");
    printf("2. Seller\n");
    printf("Enter your choice:\n");
    scanf("%d", &role_choice);
    while (getchar() != '\n'); // Clear the buffer

    if (role_choice == 1) {
        users[num_users].role = BUYER;
    } else if (role_choice == 2) {
        if (num_sellers >= MAX_SELLERS) {
            printf("Sorry, we don't need new sellers anymore ...\n");
            return;
        } else {
            users[num_users].role = BUYER;
            num_sellers++;
        }        
    } else {
        printf("Invalid choice.\n");
        return;
    }


    get_input("Enter a username:\n", username, MAX_USERNAME_LENGTH);

    // Vérifiez si le nom d'utilisateur existe déjà
    for (int i = 0; i < num_users; i++) {
        if (strcmp(users[i].username, username) == 0) {
            printf("Username already exists. Please choose another one.\n");
            return;
        }
    }

    strcpy(users[num_users].username, username);
    users[num_users].balance = 100;
    get_input("Enter a password:\n", users[num_users].password, MAX_PASSWORD_LENGTH);
    get_input("Enter a description:\n", users[num_users].description, MAX_DESCRIPTION_LENGTH);

    num_users++;

    printf("Account created successfully.\n");
}

///////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////// Shop Functions /////////////////////////////////////////

typedef struct {
    char name[30];
    char data[30];
    int price;
    char seller[MAX_USERNAME_LENGTH];
} Item;

#define MAX_ITEMS 20
Item shop[MAX_ITEMS] = {
    {"Owner's password", "", 10000000, "owner"},
};

int num_items = 1;

void check_balance() {
    if (!current_user) {
        printf("Please login first.\n");
        return;
    }
    printf("Your balance: %u\n", current_user->balance);
}

void view_shop() {
    if (!current_user) {
        printf("Please login first.\n");
        return;
    }

    printf("Items for sale:\n");
    for (int i = 0; i < num_items; i++) {
        printf("%d. %s - $%d (Seller: %s)\n", i + 1, shop[i].name, shop[i].price, shop[i].seller);
    }
}

void sell_item() {
    if (!current_user || current_user->role != SELLER) {
        printf("Only sellers can sell items.\n");
        return;
    }

    if (num_items >= MAX_ITEMS) {
        printf("The shop is full. Cannot add more items.\n");
        return;
    }

    Item newItem;
    get_input("Enter item name: \n", newItem.name, sizeof(newItem.name));
    get_input("Enter item data: \n", newItem.data, sizeof(newItem.data));
    printf("Enter item price: \n");
    scanf("%d", &newItem.price);
    while (getchar() != '\n'); // Clear the buffer

    strcpy(newItem.seller, current_user->username);
    shop[num_items++] = newItem;

    printf("Item listed for sale successfully.\n");
}

void buy_item() {
    if (!current_user || current_user->role != BUYER) {
        printf("Only buyers can buy items.\n");
        return;
    }

    view_shop();
    printf("Enter the number of the item you want to buy: \n");
    int item_index;
    scanf("%d", &item_index);
    while (getchar() != '\n'); // Clear the buffer

    if (item_index < 1 || item_index > num_items) {
        printf("Invalid item number.\n");
        return;
    }

    Item *item = &shop[item_index - 1];

    if (current_user->balance < item->price) {
        printf("Insufficient balance to buy this item.\n");
        return;
    }

    current_user->balance -= item->price;

    // Update seller balance
    for (int i = 0; i < num_users; i++) {
        if (strcmp(users[i].username, item->seller) == 0) {
            users[i].balance += item->price;
            break;
        }
    }

    // Remove the item from the shop
    for (int i = item_index - 1; i < num_items - 1; i++) {
        shop[i] = shop[i + 1];
    }
    num_items--;

    printf("Item purchased successfully.\n");
    printf("Here is the content: %s\n", item -> data);
}

///////////////////////////////////////////////////////////////////////////////////////////////


/////////////////////////////////////// Admin Functions ///////////////////////////////////////
#define MAX_NOTES 100
#define MAX_MESSAGES 10

typedef struct {
    char title[20];
    char content[256];
} Note;

Note* notes[MAX_NOTES];

typedef struct {
    char title[64];
    char message[200];
    void (*send_func)();
} Message;

Message* messages[MAX_MESSAGES];

void send_message(char *title) {
    printf("Message envoyé: %s\n", title);
}

void send_messages() {
    for (int i = 0; i < MAX_MESSAGES; i++) {
        if (messages[i] != NULL) {
            messages[i] -> send_func(messages[i] -> title);
            free(messages[i]);
            messages[i] = NULL;
        }
    }
}

void add_message() {
    for (int i = 0; i < MAX_MESSAGES; i++) {
        if (messages[i] == NULL) {
            messages[i] = (Message*)malloc(sizeof(Message));
            printf("Enter message title: \n");
            fgets(messages[i]->title, sizeof(messages[i]->title), stdin);
            strtok(messages[i]->title, "\n");  // Remove newline character
            printf("Enter message content: \n");
            fgets(messages[i]->message, sizeof(messages[i]->message), stdin);
            strtok(messages[i]->message, "\n");  // Remove newline character
            messages[i]->send_func = send_message;
            printf("Message %d created\n", i + 1);
            return;
        }
    }
    printf("No space for new message\n");
}

void add_note() {
    for (int i = 0; i < MAX_NOTES; i++) {
        if (notes[i] == NULL) {
            notes[i] = (Note*)malloc(sizeof(Note));

            printf("Enter title: \n");
            fgets(notes[i]->title, sizeof(notes[i]->title), stdin);

            printf("Enter note content: \n");
            fgets(notes[i]->content, sizeof(notes[i]->content), stdin);
            
            printf("Note created: ");
            printf(notes[i] -> title);

            return;
        }
    }
    printf("No space for new note\n");
}

void delete_note() {
    int index;
    char confirmation[3];

    printf("Enter note index to delete: \n");
    scanf("%d", &index);
    getchar();
    index--;
    if (index < 0 || index >= MAX_NOTES || notes[index] == NULL) {
        printf("Invalid index\n");
        return;
    }
    free(notes[index]);

    printf("Are you sure ? (y/n)\n");
    scanf("%2s", &confirmation);
    getchar();

    if (strcmp(confirmation, "y") == 0){
        notes[index] = NULL;
        printf("Note %d deleted\n", index + 1);
    } else {
        printf("Deletion arbored\n");
    }
}

void delete_message() {
    int index;
    printf("Enter message index to delete: \n");
    scanf("%d", &index);
    getchar();
    index--;
    if (index < 0 || index >= MAX_MESSAGES || messages[index] == NULL) {
        printf("Invalid index\n");
        return;
    }
    free(messages[index]);
    messages[index] = NULL;
    printf("Message %d deleted\n", index + 1); 
}


void display_notes() {
    printf("All notes:\n");
    for (int i = 0; i < MAX_NOTES; i++) {
        if (notes[i] != NULL) {
            printf("Note %d: %s\n", i + 1, notes[i]->content);
        }
    }
}

void edit_note() {
    int index;
    printf("Enter note index to edit: \n");
    scanf("%d", &index);
    getchar();
    index--; 
    if (index < 0 || index >= MAX_NOTES || notes[index] == NULL) {
        printf("Invalid index\n");
        return;
    }
    printf("Enter new note title: \n");
    fgets(notes[index]->title, sizeof(notes[index]->title), stdin);
    strtok(notes[index]->title, "\n");

    printf("Enter new note content: \n");
    fgets(notes[index]->content, sizeof(notes[index]->content), stdin);
    strtok(notes[index]->content, "\n");
    printf("Note %d edited\n", index + 1);
}

///////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////// Utils Functions ////////////////////////////////////////

void print_menu() {
    printf("###############################################\n");

    // If not logged
    if (!current_user) {
        printf("1. Login\n");
        printf("2. Register\n");
        printf("3. Quit\n");
    } else if (strcmp(current_user->username, "owner") == 0){ // Else If admin
        printf("1. Add a note for the future owner\n");
        printf("2. Remove a note\n");
        printf("3. View notes\n");
        printf("4. Add a message for the future owner\n");
        printf("5. Remove a message\n");
        printf("6. Send messages\n");
        printf("7. Edit a note\n");
        printf("8. Logout\n");

    } else { // Else is logged
        printf("1. Check balance\n");
        printf("2. View shop\n");
        printf("3. Sell item (Seller only)\n");
        printf("4. Buy item (Buyer only)\n");
        printf("5. Logout\n");
    }

    printf("Enter your choice: \n");
}


void init() {
    // Init owner account & owner product
    char *admin_password = getenv("ADMIN_PASSWORD");
    if (admin_password != NULL) {
        strncpy(users[0].password, admin_password, sizeof(users[0].password) - 1);
        strncpy(shop[0].data, admin_password, sizeof(shop[0].data) - 1);

        users[0].password[sizeof(users[0].password) - 1] = '\0';
        shop[0].data[sizeof(shop[0].data) - 1] = '\0';
    } else {
        printf("ERROR: ADMIN_PASSWORD environment variable not set.\n");
        exit(-1);
    }
}

int main() {
    init();
    int choice;
    while (1) {
        print_menu();
        scanf("%d", &choice);
        while (getchar() != '\n'); // Clear the buffer

        // If not logged
        if (!current_user) {
            switch (choice) {
                case 1:
                    login();
                    break;
                case 2:
                    create_account();
                    break;
                case 3:
                    printf("User disconnected.\n");
                    current_user = NULL;
                    break;
                default:
                    printf("Invalid choice!\n");
            }
        } else if (strcmp(current_user->username, "owner") == 0) {  // Else If admin
            switch (choice) {
                case 1:
                    add_note();
                    break;
                case 2:
                    delete_note();
                    break;
                case 3:
                    display_notes();
                    break;
                case 4:
                    add_message();
                    break;
                case 5:
                    delete_message();
                    break;
                case 6:
                    send_messages();
                    break;
                case 7:
                    edit_note();
                    break;
                case 8:
                    printf("Goodbye!\n");
                    current_user = NULL;
                    exit(0);
                default:
                    printf("Invalid choice!\n");
            }
        } 
        else {          // Else is logged
            switch (choice) {
                case 1:
                    check_balance();
                    break;
                case 2:
                    view_shop();
                    break;
                case 3:
                    if (current_user && current_user->role == SELLER) {
                        sell_item();
                    } else {
                        printf("Only sellers can perform this action.\n");
                    }
                    break;
                case 4:
                    if (current_user && current_user->role == BUYER) {
                        buy_item();
                    } else {
                        printf("Only buyers can perform this action.\n");
                    }
                    break;
                case 5:
                    printf("User disconnected.\n");
                    current_user = NULL;
                    break;
                default:
                    printf("Invalid choice!\n");

            }
        }
    }
    return 0;
}

///////////////////////////////////////////////////////////////////////////////////////////////